from dataclasses import dataclass
from typing import (
    Any,
    Callable,
    Generator,
    Literal,
    Optional,
    Self,
    Type,
    TypedDict,
    overload,
)

from beet import Context
from beet.core.utils import JsonDict, required_field
from bolt import AstCall, AstFormatString, AstIdentifier, AstValue
from mecha import (
    AbstractNode,
    AstNbtCompound,
    AstNbtPath,
    AstNbtPathKey,
    AstNbtPathSubscript,
    AstNode,
    AstNumber,
    AstResourceLocation,
    Mecha,
    CommandTree,
    MultilineParser,
    NbtPathParser,
    Rule,
    delegate,
    rule,
)
from mecha.utils import QuoteHelper, number_to_string
from bolt.pattern import STRING_PATTERN, RESOURCE_LOCATION_PATTERN
from tokenstream import TokenStream, Token, set_location, InvalidSyntax

FUNCTION_OVERRIDES = [
    "average",
    "binomial",
    "conditional",
    "maximum",
    "minimum",
    "uniform",
    "sum",
    "product",
]


def iter_compute_tree(tree: CommandTree):
    if tree.children:
        compute = tree.children["compute"]
        if compute.children:
            yield compute

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
                                        yield compute


@dataclass
class MutableDepth:
    value: int


type AstComputeSource = AstComputeStorage  # future AstScoreStorage

type ValueType = (
    AstComputeSource 
    | AstComputeResourceLocation 
    | AstComputeNumber 
    | AstComputeBoltValue 
    | AstComputeOperation 
    | AstComputeListCall
    | AstComputeBinomial
    | AstComputeUniform
)
type Operation = Literal["+", "-", "/", "*"]



@dataclass(frozen=True, slots=True)
class AstBoltComputeRoot(AstNode):
    children: AstComputeOperation = required_field()


@dataclass(frozen=True, slots=True)
class AstComputeStorage(AstNode):
    """Ast bolt compute storage node."""

    storage: AstComputeResourceLocation = required_field()
    path: AstNbtPath = required_field()
    depth: MutableDepth = required_field()

    @classmethod
    def from_value(
        cls,
        storage: AstComputeResourceLocation,
        path: AstNbtPath,
        depth: int,
    ) -> AstComputeStorage:
        """Return a bool node from the given value."""
        return AstComputeStorage(storage=storage, path=path, depth=MutableDepth(depth))


@dataclass(frozen=True, slots=True)
class AstComputeBoltValue(AstNode):
    value: AstNode = required_field()
    depth: MutableDepth = required_field()

    @classmethod
    def from_value(
        cls,
        value: AstNode,
        depth: int,
    ) -> Self:
        return cls(value=value, depth=MutableDepth(depth))


@dataclass(frozen=True, slots=True)
class AstComputeListCall(AstNode):
    type: str = required_field()
    operands: list[ValueType] = required_field()
    depth: MutableDepth = required_field()

    @classmethod
    def from_value(
        cls,
        type: str,
        operands: list[ValueType],
        depth: int,
    ) -> Self:
        """Return a bool node from the given value."""
        return cls(type=type, operands=operands, depth=MutableDepth(depth))


@dataclass(frozen=True, slots=True)
class AstComputeBinomial(AstNode):
    n: ValueType = required_field()
    p: ValueType = required_field()
    depth: MutableDepth = required_field()

    @classmethod
    def from_value(
        cls,
        n: ValueType,
        p: ValueType,
        depth: int,
    ) -> Self:
        return cls(n=n, p=p, depth=MutableDepth(depth))


@dataclass(frozen=True, slots=True)
class AstComputeUniform(AstNode):
    minimum: ValueType = required_field()
    maximum: ValueType = required_field()
    depth: MutableDepth = required_field()

    @classmethod
    def from_value(
        cls,
        minimum: ValueType,
        maximum: ValueType,
        depth: int,
    ) -> Self:
        return cls(minimum=minimum, maximum=maximum, depth=MutableDepth(depth))

@dataclass(frozen=True, slots=True)
class AstComputeConditional(AstNode):
    condition: AstNbtCompound      = required_field()
    on_true:   ValueType           = required_field()
    on_false:  Optional[ValueType] = required_field()
    depth:     MutableDepth        = required_field()

    @classmethod
    def from_value(
        cls,
        condition: AstNbtCompound,
        on_true: ValueType,
        on_false: Optional[ValueType],
        depth: int,
    ) -> Self:
        return cls(
            condition=condition,
            on_true=on_true,
            on_false=on_false,
            depth=MutableDepth(depth),
        )


@dataclass(frozen=True, slots=True)
class AstComputeNumber(AstNode):
    value: AstNumber = required_field()
    depth: MutableDepth = required_field()

    @classmethod
    def from_value(
        cls,
        value: Any,
        depth: int,
    ) -> Self:
        """Return a bool node from the given value."""
        return cls(value=AstNumber.from_value(value), depth=MutableDepth(depth))



@dataclass(frozen=True, slots=True)
class AstComputeResourceLocation(AstNode):
    resource_location: AstResourceLocation = required_field()
    depth: MutableDepth = required_field()

    @classmethod
    def from_value(cls, value: Any, depth: int) -> "AstComputeResourceLocation":
        return AstComputeResourceLocation(
            resource_location=AstResourceLocation.from_value(value),
            depth=MutableDepth(depth),
        )


@dataclass(frozen=True, slots=True)
class AstComputeOperation(AstNode):
    """Ast bolt compute node."""

    lvalue: ValueType = required_field()
    operation: Optional[Operation] = required_field()
    rvalue: Optional[ValueType] = required_field()

    depth: MutableDepth = required_field()

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
        return AstComputeOperation(
            lvalue=lvalue, operation=operation, rvalue=rvalue, depth=MutableDepth(depth)
        )


def parse_operation(stream: TokenStream, depth: int) -> AstComputeOperation:
    """Parse operations with correct precedence: additive (lower) then multiplicative (higher)."""
    return parse_additive(stream, depth)


def parse_additive(stream: TokenStream, depth: int) -> AstComputeOperation:
    """Parse additive operations (+, -) - lowest precedence."""
    lvalue = parse_multiplicative(stream, depth)

    while True:
        with stream.alternative():
            token = stream.expect("additive")
            rvalue = parse_multiplicative(stream, depth + 1)
            op: Operation = token.value  # pyright: ignore[reportAssignmentType]
            lvalue = AstComputeOperation.from_value(lvalue, op, rvalue, depth=depth)
            lvalue.lvalue.depth.value += 1
            continue
        break

    return lvalue


def parse_multiplicative(stream: TokenStream, depth: int) -> AstComputeOperation:
    """Parse multiplicative operations (*, /) - highest precedence."""
    lvalue = parse_primary(stream, depth)

    while True:
        with stream.alternative():
            token = stream.expect("multiplicative")
            rvalue = parse_primary(stream, depth + 1)
            op: Operation = token.value  # pyright: ignore[reportAssignmentType]
            lvalue = AstComputeOperation.from_value(lvalue, op, rvalue, depth=depth)
            lvalue.lvalue.depth.value += 1
            continue
        break

    return lvalue


def parse_primary(stream: TokenStream, depth: int) -> ValueType:
    """Parse primary expressions (literals, parenthesized expressions, function calls)."""
    with stream.checkpoint() as commit:
        stream.expect("oparent")
        result = parse_additive(stream, depth=depth)
        stream.expect("cparent")
        commit()
        return result

    return parse_literal(stream, depth=depth)


def parse_list(stream: TokenStream, depth: int):
    """Parse a comma-separated list of expressions inside brackets."""
    stream.expect("obracket")
    values: list[ValueType] = []
    while True:
        with stream.checkpoint() as commit:
            stream.expect("cbracket")
            commit()
            break
        values.append(parse_operation(stream, depth=depth + 1))
        follow = stream.expect_any("comma", "cbracket")
        match follow:
            case Token("cbracket"):
                break
            case Token("comma"):
                ...
    return values


def parse_literal(stream: TokenStream, depth: int = 0) -> ValueType:
    bolt_expression_parser = delegate("bolt:primary")
    with stream.checkpoint() as commit:
        bolt_node: AstNode = bolt_expression_parser(stream)
        # parse and return value type
        if isinstance(bolt_node, AstValue):
            if isinstance(bolt_node.value, (float, int)):
                commit()
                return AstComputeNumber.from_value(bolt_node.value, depth=depth)
            elif isinstance(bolt_node.value, str):
                commit()
                return AstComputeResourceLocation.from_value(
                    bolt_node.value, depth=depth
                )
        elif isinstance(bolt_node, AstIdentifier):
            commit()
            return AstComputeBoltValue.from_value(bolt_node, depth=depth)
        elif isinstance(bolt_node, AstFormatString):
            commit()
            return AstComputeBoltValue.from_value(bolt_node, depth=depth)
        elif isinstance(bolt_node, AstCall):
            if (
                isinstance(bolt_node.value, AstIdentifier)
                and bolt_node.value.value in FUNCTION_OVERRIDES
            ):
                raise InvalidSyntax(
                    f"Python built-in sum collide with bolt_compute sum"
                )
            commit()
            return AstComputeBoltValue.from_value(bolt_node, depth=depth)

        raise NotImplementedError(bolt_node)

    stream.crop()
    token = stream.expect_any("oparent", "number", "quotes", "storage", "call")
    match token:
        case Token("oparent"):
            return parse_operation(stream, depth=depth + 1)
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
        case Token("call"):
            if token.value in ["maximum", "minimum", "average", "sum", "product"]:
                stream.expect("oparent")
                values = parse_list(stream, depth + 1)
                if len(values) == 0:
                    raise InvalidSyntax(
                        f"Function {token.value} require at least one argument"
                    )
                stream.expect("cparent")
                return AstComputeListCall.from_value(token.value, values, depth)
            elif token.value == "binomial":
                stream.expect("oparent")
                N = parse_literal(stream, depth=depth + 1)
                stream.expect("comma")
                P = parse_literal(stream, depth=depth + 1)
                cparent, comma = stream.expect("cparent", "comma")
                if comma:
                    stream.expect("cparent")
                return AstComputeBinomial.from_value(N, P, depth)
            elif token.value == "uniform":
                stream.expect("oparent")
                minimum = parse_literal(stream, depth=depth + 1)
                stream.expect("comma")
                maximum = parse_literal(stream, depth=depth + 1)
                cparent, comma = stream.expect("cparent", "comma")
                if comma:
                    stream.expect("cparent")
                return AstComputeUniform.from_value(minimum, maximum, depth)
            elif token.value == "conditional":
                stream.expect("oparent")
                condition = delegate("resource_location_or_nbt")(stream)
                stream.expect("comma")
                on_true = parse_literal(stream, depth=depth + 1)

                cparent, comma = stream.expect("cparent", "comma")
                if comma:
                    with stream.checkpoint() as commit:
                        stream.expect("cparent")
                        commit()
                        return AstComputeConditional.from_value(condition, on_true, None, depth)

                on_false = parse_literal(stream, depth=depth + 1)
                cparent, comma = stream.expect("cparent", "comma")
                if comma:
                    stream.expect("cparent")
                return AstComputeConditional.from_value(condition, on_true, on_false, depth)


            raise NotImplementedError(token.value)

    raise NotImplementedError("UNREACHABLE")


def operation_parser(stream: TokenStream):
    """Parse operation."""
    with stream.syntax(bolt="bolt"):
        stream.expect("bolt")
    with stream.syntax(
        oparent=r"\(",
        cparent=r"\)",
        obracket=r"\[",
        cbracket=r"\]",
        comma=r",",
        equal=r"=",
        additive=r"\+|\-",
        multiplicative=r"\*|\/",
        number=r"[+-]?([0-9]*[.])?[0-9]+",
        storage=r"storage",
        call="|".join(FUNCTION_OVERRIDES),
        quotes=r'"',
        resource=RESOURCE_LOCATION_PATTERN,
        name=r"[a-z]([a-z0-9]+)?",
    ):
        stream.expect("oparent")
        operation = parse_operation(stream, depth=0)
        stream.expect("cparent", "end")
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
                result.append(",")
                yield node.rvalue
                result.append("]}")
            case "-":
                result.append('{type:"minecraft:sum",operands:[')
                yield node.lvalue
                result.append(",")
                result.append('{type:"minecraft:product",operands:[-1')
                result.append(",")
                yield node.rvalue
                result.append("]}")
                result.append("]}")
            case "*":
                result.append('{type:"minecraft:product",operands:[')
                yield node.lvalue
                result.append(",")
                yield node.rvalue
                result.append("]}")
            case _:
                raise NotImplementedError()


@rule(AstBoltComputeRoot)
def serialize_root(node: AstBoltComputeRoot, result: list[str]):
    result.append("default")
    result.append(" ")
    yield node.children


@rule(AstComputeResourceLocation)
def serialize_resource_location(node: AstComputeResourceLocation, result: list[str]):
    if node.depth.value != 0:
        result.append('"')
    result.append(node.resource_location.get_canonical_value())
    if node.depth.value != 0:
        result.append('"')


@rule(AstComputeStorage)
def serialize_storage(node: AstComputeStorage, result: list[str]):
    result.append('{type:"minecraft:storage",storage:"')
    yield node.storage
    result.append('",path:"')
    yield node.path
    result.append('"}')


@rule(AstComputeBoltValue)
def serialize_bolt_value(node: AstComputeBoltValue, result: list[str]):
    if isinstance(node.value, (float, int)):
        yield AstComputeNumber.from_value(node.value, node.depth.value)
    elif isinstance(node.value, str):
        a = AstComputeResourceLocation.from_value(node.value, node.depth.value)
        yield a


@rule(AstComputeListCall)
def serialize_list_call(node: AstComputeListCall, result: list[str]):
    result.append('{type:"minecraft:')
    result.append(node.type)
    result.append('",operands:[')
    sep = ""
    for children in node.operands:
        result.append(sep)
        sep = ","
        yield children
    result.append("]}")


@rule(AstComputeNumber)
def serialize_compute_number(node: AstComputeNumber, result: list[str]):
    if node.depth.value == 0:
        result.append('{type:"minecraft:constant",value:')
    yield node.value
    if node.depth.value == 0:
        result.append("}")


@rule(AstComputeBinomial)
def serialize_compute_binomial(node: AstComputeBinomial, result: list[str]):
    result.append('{type:"minecraft:binomial",n:')
    yield node.n
    result.append(",p:")
    yield node.p
    result.append("}")


@rule(AstComputeUniform)
def serialize_compute_uniform(node: AstComputeUniform, result: list[str]):
    result.append('{type:"minecraft:uniform",min:')
    yield node.minimum
    result.append(",max:")
    yield node.maximum
    result.append("}")


@rule(AstComputeConditional)
def serialize_compute_conditional(node: AstComputeConditional, result: list[str]):
    result.append('{type:"minecraft:conditional",condition:')
    yield node.condition
    result.append(",on_true:")
    yield node.on_true
    if node.on_false:
        result.append(',on_false:')
        yield node.on_false
    result.append("}")


def beet_default(ctx: Context):
    mc = ctx.inject(Mecha)
    mc.spec.parsers["command:argument:minecraft:number_provider"] = MultilineParser(
        delegate("resource_location_or_nbt")
    )
    rules = [
        serialize_operation,
        serialize_resource_location,
        serialize_root,
        serialize_storage,
        serialize_bolt_value,
        serialize_compute_number,
        serialize_list_call,
        serialize_compute_binomial,
        serialize_compute_uniform,
        serialize_compute_conditional,
    ]
    for r in rules:
        mc.serialize.add_rule(r)

    for compute in iter_compute_tree(mc.spec.tree):
        if compute.children:
            compute.children["bolt"] = CommandTree(
                **{
                    "type": "argument",
                    "executable": True,
                    "parser": "bolt_compute:operation_parser",
                }
            )

    mc.spec.parsers["command:argument:bolt_compute:operation_parser"] = MultilineParser(
        operation_parser
    )

    mc.spec.update()
