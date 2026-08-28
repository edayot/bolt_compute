from dataclasses import dataclass
from typing import Any, Callable, Generator, Literal, Optional, Self, Type, TypedDict, overload

from beet import Context
from beet.core.utils import JsonDict, required_field
from bolt import AstFormatString, AstIdentifier, AstValue
from mecha import AbstractNode, AstNbtPath, AstNbtPathKey, AstNbtPathSubscript, AstNode, AstNumber, AstResourceLocation, Mecha, CommandTree, MultilineParser, NbtPathParser, Rule, delegate, rule
from mecha.utils import QuoteHelper, number_to_string
from bolt.pattern import STRING_PATTERN, RESOURCE_LOCATION_PATTERN
from tokenstream import TokenStream, Token, set_location, InvalidSyntax

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
class AstComputeStorage(AstNode):
    """Ast bolt compute storage node."""
    storage: AstComputeResourceLocation = required_field()
    path: AstNbtPath = required_field()
    depth: int = required_field()

    @classmethod
    def from_value(
        cls,
        storage: AstComputeResourceLocation,
        path: AstNbtPath,
        depth: int,
    ) -> AstComputeStorage:
        """Return a bool node from the given value."""
        return AstComputeStorage(storage=storage, path=path, depth=depth)

@dataclass(frozen=True, slots=True)
class AstComputeIdentifier(AstNode):
    value: AstIdentifier = required_field()
    depth: int = required_field()

    @classmethod
    def from_value(
        cls,
        value: AstIdentifier,
        depth: int,
    ) -> Self:
        return cls(value=value, depth=depth)

@dataclass(frozen=True, slots=True)
class AstComputeFormatString(AstNode):
    value: AstFormatString = required_field()
    depth: int = required_field()

    @classmethod
    def from_value(
        cls,
        value: AstFormatString,
        depth: int,
    ) -> Self:
        return cls(value=value, depth=depth)

@dataclass(frozen=True, slots=True)
class AstComputeNumber(AstNode):
    value: AstNumber = required_field()
    depth: int = required_field()

    @classmethod
    def from_value(
        cls,
        value: Any,
        depth: int,
    ) -> Self:
        """Return a bool node from the given value."""
        return cls(value=AstNumber.from_value(value), depth=depth)



type AstComputeSource = AstComputeStorage # future AstScoreStorage

type ValueType = AstComputeOperation | AstComputeResourceLocation | AstComputeNumber | AstComputeSource | AstComputeIdentifier
type Operation = Literal["+", "-", "/", "*"]

@dataclass(frozen=True, slots=True)
class AstBoltComputeRoot(AstNode):
    children: AstComputeOperation = required_field()

@dataclass(frozen=True, slots=True)
class AstComputeResourceLocation(AstNode): 
    resource_location: AstResourceLocation = required_field()
    depth: int = required_field()

    @classmethod
    def from_value(cls, value: Any, depth: int) -> "AstComputeResourceLocation": 
        return AstComputeResourceLocation(resource_location=AstResourceLocation.from_value(value), depth=depth)

@dataclass(frozen=True, slots=True)
class AstComputeOperation(AstNode):
    """Ast bolt compute node."""

    lvalue: ValueType = required_field()
    operation: Optional[Operation] = required_field()
    rvalue: Optional[ValueType] = required_field()

    depth: int = required_field()

    parser = "bolt_compute:parse_operation"

    @classmethod
    def from_value(
        cls,
        lvalue: ValueType,
        operation: Optional[Operation] = None,
        rvalue: Optional[ValueType] = None,
        depth: int = 0,
    ) -> AstComputeOperation:
        """Return a bool node from the given value."""
        return AstComputeOperation(lvalue=lvalue, operation=operation, rvalue=rvalue, depth=depth)


def parse_operation(stream: TokenStream, depth: int) -> AstComputeOperation:
    with stream.checkpoint() as commit:
        lvalue = parse_literal(stream, depth=depth)
        stream.expect("cparent")
        commit()
        return AstComputeOperation.from_value(lvalue, depth=depth)
    
    lvalue = parse_literal(stream, depth=depth+1)
    token = stream.expect("operation")
    rvalue = parse_operation(stream, depth=depth+1)
    op: Operation = token.value # pyright: ignore[reportAssignmentType]
    return AstComputeOperation.from_value(lvalue, op, rvalue, depth=depth)
    raise NotImplementedError("UNREACHABLE")


def parse_literal(stream: TokenStream, depth: int = 0) -> ValueType:
    with stream.checkpoint() as commit:
        bolt_expression_parser = delegate("bolt:primary")
        bolt_node: AstValue | AstIdentifier = bolt_expression_parser(stream)
        # parse and return value type
        if isinstance(bolt_node, AstValue):
            if isinstance(bolt_node.value, (float, int)):
                commit()
                return AstComputeNumber.from_value(bolt_node.value, depth=depth)
            elif isinstance(bolt_node.value, str):
                commit()
                return AstComputeResourceLocation.from_value(bolt_node.value, depth=depth)
        elif isinstance(bolt_node, AstIdentifier):
            commit()
            return AstComputeIdentifier.from_value(bolt_node, depth=depth)
        elif isinstance(bolt_node, AstFormatString):
            commit()
            return AstComputeFormatString.from_value(bolt_node, depth=depth)
        raise NotImplementedError(bolt_node)

    stream.crop()
    token = stream.expect_any("oparent", "number", "quotes", "storage")
    match token:
        case Token("oparent"):
            return parse_operation(stream, depth=depth+1)
        case Token("number"):
            return AstComputeNumber.from_value(token.value, depth=depth)
        case Token("quotes"):
            res: AstResourceLocation = delegate("resource_location")(stream)
            stream.expect("quotes")
            return AstComputeResourceLocation.from_value(res, depth=depth)
        case Token("storage"):
            storage: AstComputeResourceLocation = delegate("resource_location")(stream)
            parser = delegate("nbt_path")
            path: AstNbtPath = parser(stream)
            return AstComputeStorage.from_value(storage, path, depth=depth)

    raise NotImplementedError("UNREACHABLE")



def operation_parser(stream: TokenStream):
    """Parse operation."""
    with stream.syntax(
        bolt="bolt"
    ):
        stream.expect("bolt")
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
        operation = parse_operation(stream, depth=0)
    return AstBoltComputeRoot(children=operation)



@rule(AstComputeOperation)
def serialize_operation(node: AstComputeOperation, result: list[str]):
    if node.lvalue and not node.rvalue:
        assert node.operation is None
        yield node.lvalue
    elif node.lvalue and node.rvalue:
        assert node.operation is not None
        match node.operation:
            case "+":
                result.append('{type:"minecraft:sum",operands:[')
                yield node.lvalue
                result.append(',')
                yield node.rvalue
                result.append(']}')
            case "-":
                result.append('{type:"minecraft:sum",operands:[')
                yield node.lvalue
                result.append(',')
                result.append('{type:"minecraft:product",operands:[-1')
                result.append(',')
                yield node.rvalue
                result.append(']}')
                result.append(']}')
            case "*":
                result.append('{type:"minecraft:product",operands:[')
                yield node.lvalue
                result.append(',')
                yield node.rvalue
                result.append(']}')
            case _:
                raise NotImplementedError()

@rule(AstBoltComputeRoot)
def serialize_root(node: AstBoltComputeRoot, result: list[str]):
    result.append("default")
    result.append(" ")
    yield node.children

@rule(AstComputeResourceLocation)
def serialize_resource_location(node: AstComputeResourceLocation, result: list[str]):
    if node.depth != 0: result.append('"')
    result.append(node.resource_location.get_canonical_value())
    if node.depth != 0: result.append('"')

@rule(AstComputeStorage)
def serialize_storage(node: AstComputeStorage, result: list[str]):
    result.append('{type:"minecraft:storage",storage:"')
    yield node.storage
    result.append('",path:"')
    yield node.path
    result.append('"}')


@rule(AstComputeIdentifier)
def serialize_compute_identifier(node: AstComputeIdentifier, result: list[str]):
    if isinstance(node.value, (float, int)):
        yield AstComputeNumber.from_value(node.value, node.depth)
    elif isinstance(node.value, str): 
        yield AstComputeResourceLocation.from_value(node.value, node.depth)

@rule(AstComputeFormatString)
def serialize_compute_format_string(node: AstComputeFormatString, result: list[str]):
    if isinstance(node.value, (float, int)):
        yield AstComputeNumber.from_value(node.value, node.depth)
    elif isinstance(node.value, str): 
        yield AstComputeResourceLocation.from_value(node.value, node.depth)



@rule(AstComputeNumber)
def serialize_compute_number(node: AstComputeNumber, result: list[str]): 
    if node.depth == 0: result.append('{type:"minecraft:constant",value:')
    yield node.value
    if node.depth == 0: result.append('}')

def beet_default(ctx: Context):
    mc = ctx.inject(Mecha)
    mc.spec.parsers["command:argument:minecraft:number_provider"] = MultilineParser(delegate("resource_location_or_nbt"))
    mc.serialize.add_rule(serialize_operation)
    mc.serialize.add_rule(serialize_resource_location)
    mc.serialize.add_rule(serialize_root)
    mc.serialize.add_rule(serialize_storage)
    mc.serialize.add_rule(serialize_compute_identifier)
    mc.serialize.add_rule(serialize_compute_number)
    mc.serialize.add_rule(serialize_compute_format_string)

    for compute in iter_compute_tree(mc.spec.tree):
        if compute.children:
            compute.children["bolt"] = CommandTree(**{
                "type": "argument",
                "executable": True,
                "parser": "bolt_compute:operation_parser"
            })

    mc.spec.parsers["command:argument:bolt_compute:operation_parser"] = MultilineParser(operation_parser)

        
    mc.spec.update()
