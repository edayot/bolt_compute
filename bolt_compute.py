from dataclasses import dataclass
from typing import Generator, Literal, Optional, TypedDict

from beet import Context
from beet.core.utils import JsonDict, required_field
from mecha import AstNode, Mecha, CommandTree, MultilineParser, delegate, rule
from mecha.utils import number_to_string
from bolt.pattern import STRING_PATTERN
from tokenstream import TokenStream, Token, set_location

import json


def iter_compute_tree(tree: CommandTree):
    if tree.children:
        data = tree.children["data"]
        if data.children:
            modify = data.children["modify"]
            if modify.children:
                childs = [
                    "block",
                    "entity",
                    "storage",
                ]
                for c in childs:
                    child = modify.children[c]
                    if child.children:
                        target = child.children["target"]
                        if target.children:
                            targetPath = target.children["targetPath"]
                            if targetPath.children:
                                for o in [
                                    "append",
                                    "merge",
                                    "prepend",
                                    "set",
                                ]:
                                    operation = targetPath.children[o]
                                    if operation.children:
                                        compute = operation.children["compute"]
                                        yield compute
                                insert = targetPath.children["insert"]
                                if insert.children:
                                    index = insert.children["index"]
                                    if index.children:
                                        compute = index.children["compute"]
                                        



class AstSource(TypedDict):
    ...

type ValueType = AstOperation | str | float | AstSource
type Operation = Literal["+", "-", "/", "*"]

@dataclass(frozen=True, slots=True)
class AstOperation(AstNode):
    """Ast bool node."""

    lvalue: ValueType = required_field()
    operation: Optional[Operation] = required_field()
    rvalue: Optional[ValueType] = required_field()

    parser = "bolt_compute:parse_operation"

    @classmethod
    def from_value(
        cls,
        lvalue: ValueType,
        operation: Optional[Operation] = None,
        rvalue: Optional[ValueType] = None,
    ) -> AstOperation:
        """Return a bool node from the given value."""
        return AstOperation(lvalue=lvalue, operation=operation, rvalue=rvalue)


def parse_operation(stream: TokenStream) -> AstOperation:
    lvalue = parse_literal(stream)
    token = stream.expect_any("cparent", "operation")
    match token:
        case Token("cparent"):
            return AstOperation.from_value(lvalue)
        case Token("operation"):
            rvalue = parse_operation(stream)
            return AstOperation.from_value(lvalue, token.value, rvalue)
    raise NotImplementedError("UNREACHABLE")


def parse_literal(stream: TokenStream) -> ValueType:
    token = stream.expect_any("oparent", "number", "quotes")
    match token:
        case Token("oparent"):
            return parse_operation(stream)
        case Token("number"):
            return float(token.value)
        case Token("quotes"):
            res = stream.expect("resource")
            stream.expect("quotes")
            return res.value
    raise NotImplementedError("UNREACHABLE")


def serialize_recursive(node: ValueType, is_first: bool = True) -> Generator[JsonDict | str | float]:
    if isinstance(node, AstOperation):
        if not node.operation:
            yield from serialize_recursive(node.lvalue, is_first = is_first)
        else:
            assert node.rvalue
            match node.operation:
                case "+":
                    yield {"type":"minecraft:sum","operands":[
                        *serialize_recursive(node.lvalue, is_first = False),
                        *serialize_recursive(node.rvalue, is_first = False)
                    ]}
                case _:
                    raise NotImplementedError()
    elif isinstance(node, float):
        if is_first:
            yield {"type":"constant","value":node}
        else:
            yield node
    elif isinstance(node, str):
        yield node

@rule(AstOperation)
def serialize_operation(node: ValueType, result: list[str]):
    result.pop()
    result.pop()
    result.append("default")
    result.append(" ")
    result.extend([json.dumps(x) for x in serialize_recursive(node)])


def operation_parser(stream: TokenStream):
    """Parse operation."""
    res = {}
    with stream.syntax(
        oparent=r"\(",
        cparent=r"\)",
        operation=r"\+|\-|\*|\/",
        number=r"[+-]?([0-9]*[.])?[0-9]+",
        quotes=r'"',
        resource=STRING_PATTERN,
    ):
        token = stream.expect("oparent")
        operation = parse_operation(stream)
    return operation
        



def beet_default(ctx: Context):
    mc = ctx.inject(Mecha)
    mc.spec.parsers["command:argument:minecraft:number_provider"] = MultilineParser(delegate("resource_location_or_nbt"))
    mc.serialize.add_rule(serialize_operation)

    for compute in iter_compute_tree(mc.spec.tree):
        if compute.children:
            compute.children["bolt"] = CommandTree(**{
                "type": "literal",
                "children": {
                    "operation": {
                        "type": "argument",
                        "executable": True,
                        "parser": "bolt_compute:operation_parser"
                    }
                }
            })

    mc.spec.parsers["command:argument:bolt_compute:operation_parser"] = MultilineParser(operation_parser)

        
    mc.spec.update()
