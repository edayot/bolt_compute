from dataclasses import dataclass
from typing import Generator, Literal, Optional, TypedDict

from beet import Context
from beet.core.utils import JsonDict, required_field
from mecha import AstNbtPath, AstNbtPathKey, AstNbtPathSubscript, AstNode, AstResourceLocation, Mecha, CommandTree, MultilineParser, NbtPathParser, delegate, rule
from mecha.utils import QuoteHelper, number_to_string
from bolt.pattern import STRING_PATTERN, RESOURCE_LOCATION_PATTERN
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
                                        

@dataclass(frozen=True, slots=True)
class AstComputeResourceLocation(AstResourceLocation): ...


@dataclass(frozen=True, slots=True)
class AstComputeStorage(AstNode):
    """Ast bolt compute storage node."""
    storage: AstComputeResourceLocation = required_field()
    path: AstNbtPath = required_field()

    @classmethod
    def from_value(
        cls,
        storage: AstComputeResourceLocation,
        path: AstNbtPath,
    ) -> AstComputeStorage:
        """Return a bool node from the given value."""
        return AstComputeStorage(storage=storage, path=path)


type AstComputeSource = AstComputeStorage

type ValueType = AstComputeOperation | AstResourceLocation | float | AstComputeSource
type Operation = Literal["+", "-", "/", "*"]

@dataclass(frozen=True, slots=True)
class AstComputeOperation(AstNode):
    """Ast bolt compute node."""

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
    ) -> AstComputeOperation:
        """Return a bool node from the given value."""
        return AstComputeOperation(lvalue=lvalue, operation=operation, rvalue=rvalue)


def parse_operation(stream: TokenStream) -> AstComputeOperation:
    lvalue = parse_literal(stream)
    token = stream.expect_any("cparent", "operation")
    match token:
        case Token("cparent"):
            return AstComputeOperation.from_value(lvalue)
        case Token("operation"):
            rvalue = parse_operation(stream)
            return AstComputeOperation.from_value(lvalue, token.value, rvalue)
    raise NotImplementedError("UNREACHABLE")


def parse_literal(stream: TokenStream) -> ValueType:
    token = stream.expect_any("oparent", "number", "quotes", "storage")
    match token:
        case Token("oparent"):
            return parse_operation(stream)
        case Token("number"):
            return float(token.value)
        case Token("quotes"):
            res: AstResourceLocation = delegate("resource_location")(stream)
            stream.expect("quotes")
            return res
        case Token("storage"):
            storage: AstResourceLocation = delegate("resource_location")(stream)
            parser = delegate("nbt_path")
            path: AstNbtPath = parser(stream)
            return AstComputeStorage.from_value(storage, path)

    raise NotImplementedError("UNREACHABLE")


def serialize_recursive(node: ValueType, is_first: bool = True) -> JsonDict | str | float:
    if isinstance(node, AstComputeOperation):
        if not node.operation:
            return serialize_recursive(node.lvalue, is_first = is_first)
        else:
            assert node.rvalue
            match node.operation:
                case "+":
                    return {
                        "type":"minecraft:sum",
                        "operands":[
                            serialize_recursive(node.lvalue, is_first = False),
                            serialize_recursive(node.rvalue, is_first = False)
                        ]
                    }
                case "-":
                    return {
                        "type":"minecraft:sum",
                        "operands":[
                            serialize_recursive(node.lvalue, is_first = False),
                            {
                                "type": "minecraft:product",
                                "operands": [
                                    -1,
                                    serialize_recursive(node.rvalue, is_first = False)
                                ]
                            },
                        ]
                    }
                case "*":
                    return {
                        "type": "minecraft:product",
                        "operands": [
                            serialize_recursive(node.lvalue, is_first = False),
                            serialize_recursive(node.rvalue, is_first = False)
                        ]
                    }
                case _:
                    raise NotImplementedError()
    elif isinstance(node, float):
        if is_first:
            return {"type":"constant","value":node}
        else:
            return node
    elif isinstance(node, AstResourceLocation):
        return node.get_canonical_value()
    elif isinstance(node, AstComputeStorage):
        res = []
        return {
            "type": "minecraft:storage",
            "storage": node.storage.get_canonical_value(),
            "path": node.path
        }
    else:
        raise NotImplementedError(node)


@rule(AstComputeOperation)
def serialize_operation(node: ValueType, result: list[str]):
    result.pop()
    result.pop()
    result.append("default")
    result.append(" ")
    result.append('{')
    result.append("}")

    res = serialize_recursive(node)
    if isinstance(res, str):
        result.append(res)
    else:
        result.extend(json.dumps(res))


def operation_parser(stream: TokenStream):
    """Parse operation."""
    res = {}
    with stream.syntax(
        oparent=r"\(",
        cparent=r"\)",
        operation=r"\+|\-|\*|\/",
        number=r"[+-]?([0-9]*[.])?[0-9]+",
        storage=r"storage",
        quotes=r'"',
        resource=RESOURCE_LOCATION_PATTERN,
    ):
        stream.expect("oparent")
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
