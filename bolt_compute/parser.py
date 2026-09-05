from typing import Literal, assert_never, cast, overload, reveal_type

from bolt import AstCall, AstFormatString, AstIdentifier, AstValue
from mecha import (
    AstNode,
    UnrecognizedParser,
    delegate,
)
from tokenstream import InvalidSyntax, Token, TokenStream, set_location

from bolt_compute.float import *
from bolt_compute.integer import *
from bolt_compute.node import AstBaseNode, AstComputeRoot, MutableDepth
from bolt_compute.types import AdditiveOperation, BoltType, MultiplicativeOperation, Operation, OperationType
from contextlib import contextmanager


SCORE_TARGETS = (
    "this",
    "attacker",
    "direct_attacker",
    "attacking_player",
    "target_entity",
    "interacting_entity",
    "fixed",
)

FUNCTIONS = (
    "abs",
    "avg",
)

@contextmanager
def integer_syntax(stream: TokenStream):
    with stream.syntax(
        oparent=r"\(",
        cparent=r"\)",
        obracket=r"\[",
        cbracket=r"\]",
        comma=r",",
        dot=r"\.",
        conditional=r"if|else",
        additive=r"\+|\-",
        multiplicative=r'\*\*' r'|\*' r'|\/\/' r'|\%',
        number=r"[+-]?[0-9]+",
        storage=r"storage",
        score=r"score",
        quotes=r'"|\'',
        target="|".join(SCORE_TARGETS),
    ):
        with stream.provide(bolt_compute_keywords={x: None for x in ["conditional", "storage", "score", "target"]}):
            yield

@contextmanager
def float_syntax(stream: TokenStream):
    with stream.syntax(
        oparent=r"\(",
        cparent=r"\)",
        obracket=r"\[",
        cbracket=r"\]",
        comma=r",",
        dot=r"\.",
        conditional=r"if|else",
        additive=r"\+|\-",
        multiplicative=r'\*\*' r'|\*' r'|\/' r'|\%',
        number=r"[+-]?([0-9]*[.])?[0-9]+",
        storage=r"storage",
        score=r"score",
        quotes=r'"|\'',
        target="|".join(SCORE_TARGETS),
    ):
        with stream.provide(bolt_compute_keywords={x: None for x in ["conditional", "storage", "score", "target"]}):
            yield

@overload
def parse_expression(stream: TokenStream, operation_type: Literal["float"], depth: int) -> AstBaseFloat: ...
@overload
def parse_expression(stream: TokenStream, operation_type: Literal["integer"], depth: int) -> AstBaseInteger: ...

def parse_expression(stream: TokenStream, operation_type: OperationType, depth: int) -> AstBaseNode:
    """Parse operations with correct precedence: additive (lower) then multiplicative (higher)."""
    return parse_conditional(stream, operation_type, depth)


@overload
def parse_conditional(stream: TokenStream, operation_type: Literal["float"], depth: int) -> AstBaseFloat: ...
@overload
def parse_conditional(stream: TokenStream, operation_type: Literal["integer"], depth: int) -> AstBaseInteger: ...

def parse_conditional(stream: TokenStream, operation_type: OperationType, depth: int) -> AstBaseNode:
    on_true = parse_additive(stream, operation_type, depth)
    while True:
        with stream.alternative():
            token = stream.expect("conditional")
            if token.value == "else": 
                exc = InvalidSyntax("Cannot have an `else` statement without a preceding `if` statement")
                set_location(exc, token)
                raise exc
            # token.value == "if"
            on_true.depth.value += 1
            condition = delegate("resource_location_or_nbt")(stream)
            
            token = stream.expect("conditional")
            if token.value == "if": 
                exc = InvalidSyntax("Cannot have an `if` statement without a preceding `else` statement")
                set_location(exc, token)
                raise exc
            
            # Recursively parse the else clause (which could be another conditional)
            on_false = parse_additive(stream, operation_type, depth+1)
            if operation_type == "integer":
                on_true = AstIntegerConditional(condition=condition, on_true=on_true.cast_int(), on_false=on_false.cast_int(), depth=MutableDepth(depth))
            elif operation_type == "float":
                on_true = AstFloatConditional(condition=condition, on_true=on_true.cast_float(), on_false=on_false.cast_float(), depth=MutableDepth(depth))
            else:
                exc = InvalidSyntax("No operation_type in current context")
                set_location(exc, on_false)
                raise exc
            set_location(on_true, token)
            continue
        break
    return on_true  


@overload
def parse_additive(stream: TokenStream, operation_type: Literal["float"], depth: int) -> AstBaseFloat: ...
@overload
def parse_additive(stream: TokenStream, operation_type: Literal["integer"], depth: int) -> AstBaseInteger: ...

def parse_additive(stream: TokenStream, operation_type: OperationType, depth: int) -> AstBaseNode:
    """Parse additive operations (+, -) - lowest precedence."""
    lvalue = parse_multiplicative(stream, operation_type, depth)

    while True:
        with stream.alternative():
            token = stream.expect("additive")
            rvalue = parse_multiplicative(stream, operation_type, depth + 1)
            lvalue.depth.value += 1
            op: AdditiveOperation = token.value  # pyright: ignore[reportAssignmentType]
            match op:
                case "+":
                    if operation_type == "integer":
                        lvalue = AstIntegerAdd(inputs=[lvalue.cast_int(), rvalue.cast_int()], depth=MutableDepth(depth))
                    elif operation_type == "float":
                        lvalue = AstFloatAdd(inputs=AstChildren([lvalue.cast_float(), rvalue.cast_float()]), depth=MutableDepth(depth))
                case "-":
                    if operation_type == "integer":
                        lvalue = AstIntegerSub(left=lvalue.cast_int(), right=rvalue.cast_int(), depth=MutableDepth(depth))
                    elif operation_type == "float":
                        lvalue = AstFloatSub(left=lvalue.cast_float(), right=rvalue.cast_float(), depth=MutableDepth(depth))
                case _:
                    assert_never("AdditiveOperation", op)

            set_location(lvalue, token)
            continue
        break

    return lvalue


@overload
def parse_multiplicative(stream: TokenStream, operation_type: Literal["float"], depth: int) -> AstBaseFloat: ...
@overload
def parse_multiplicative(stream: TokenStream, operation_type: Literal["integer"], depth: int) -> AstBaseInteger: ...


def parse_multiplicative(stream: TokenStream, operation_type: OperationType, depth: int) -> AstBaseNode:
    """Parse multiplicative operations (*, /) - highest precedence."""
    lvalue = parse_primary(stream, operation_type, depth)

    while True:
        with stream.alternative():
            token = stream.expect("multiplicative")
            rvalue = parse_primary(stream, operation_type, depth + 1)
            lvalue.depth.value += 1
            op: MultiplicativeOperation = token.value  # pyright: ignore[reportAssignmentType]
            match op:
                case "*":
                    if operation_type == "integer":
                        lvalue = AstIntegerMul(inputs=[lvalue.cast_int(), rvalue.cast_int()], depth=MutableDepth(depth))
                    elif operation_type == "float":
                        lvalue = AstFloatMul(inputs=AstChildren([lvalue.cast_float(), rvalue.cast_float()]), depth=MutableDepth(depth))
                case "**":
                    if operation_type == "integer":
                        lvalue = AstIntegerPow(left=lvalue.cast_int(), right=rvalue.cast_int(), depth=MutableDepth(depth))
                    elif operation_type == "float":
                        lvalue = AstFloatPow(left=lvalue.cast_float(), right=rvalue.cast_float(), depth=MutableDepth(depth))
                case "/":
                    assert (operation_type == "float")
                    lvalue = AstFloatDiv(left=lvalue.cast_float(), right=rvalue.cast_float(), depth=MutableDepth(depth))
                case "//":
                    assert (operation_type == "integer")
                    lvalue = AstIntegerDiv(left=lvalue.cast_int(), right=rvalue.cast_int(), depth=MutableDepth(depth))
                case "%":
                    if operation_type == "integer":
                        lvalue = AstIntegerMod(left=lvalue.cast_int(), right=rvalue.cast_int(), depth=MutableDepth(depth))
                    elif operation_type == "float":
                        lvalue = AstFloatMod(left=lvalue.cast_float(), right=rvalue.cast_float(), depth=MutableDepth(depth))
                case _:
                    assert_never("MultiplicativeOperation", op)
            set_location(lvalue, token)
            continue
        break

    return lvalue

@overload
def parse_primary(stream: TokenStream, operation_type: Literal["float"], depth: int) -> AstBaseFloat: ...
@overload
def parse_primary(stream: TokenStream, operation_type: Literal["integer"], depth: int) -> AstBaseInteger: ...

def parse_primary(stream: TokenStream, operation_type: OperationType, depth: int) -> AstBaseNode:
    """Parse primary expressions (literals, parenthesized expressions, function calls)."""
    with stream.checkpoint() as commit:
        stream.expect("oparent")
        commit()
        result = parse_expression(stream, operation_type, depth=depth)
        commit()
        stream.expect("cparent")
        commit()
        return result

    return parse_literal(stream, operation_type, depth=depth)

@overload
def parse_literal(stream: TokenStream, operation_type: Literal["float"], depth: int) -> AstBaseFloat: ...
@overload
def parse_literal(stream: TokenStream, operation_type: Literal["integer"], depth: int) -> AstBaseInteger: ...
def parse_literal(stream: TokenStream, operation_type: OperationType, depth: int) -> AstBaseNode: 
    bolt_expression_parser = delegate("bolt:primary")
    with stream.checkpoint() as commit:
        try:
            bolt_node: AstNode = bolt_expression_parser(stream)
        except UnrecognizedParser:
            raise InvalidSyntax("Bolt is not loaded")
        if isinstance(bolt_node, AstValue):
            if isinstance(bolt_node.value, (float, int)) and operation_type == "float":
                commit()
                node = AstFloatConstant(value=float(bolt_node.value), depth=MutableDepth(depth))
                set_location(node, bolt_node)
                return node
            elif isinstance(bolt_node.value, int) and operation_type == "integer":
                commit()
                node = AstIntegerConstant(value=int(bolt_node.value), depth=MutableDepth(depth))
                set_location(node, bolt_node)
                return node
            elif isinstance(bolt_node.value, str):
                if operation_type == "float":
                    commit()
                    node = AstFloatReference(reference=bolt_node.value, depth=MutableDepth(depth))
                    set_location(node, bolt_node)
                    return node
                elif operation_type == "integer":
                    commit()
                    node = AstIntegerReference(reference=bolt_node.value, depth=MutableDepth(depth))
                    set_location(node, bolt_node)
                    return node
        elif isinstance(bolt_node, (AstIdentifier, AstFormatString)):
            if operation_type == "integer":
                commit()
                node = AstIntegerBoltVariable(value=bolt_node, depth=MutableDepth(depth))
                set_location(node, bolt_node)
                return node
            elif operation_type == "float":
                commit()
                node = AstFloatBoltVariable(value=bolt_node, depth=MutableDepth(depth))
                set_location(node, bolt_node)
                return node
        elif isinstance(bolt_node, AstCall):
            exc = InvalidSyntax("Bolt calls are not allowed")
            set_location(exc, bolt_node)
            raise exc
        raise NotImplementedError(bolt_node)

    stream.crop()

    token = stream.expect_any("number", "quotes", "storage", "score")
    match token:
        case Token("number"):
            if operation_type == "float":
                node = AstFloatConstant(value=float(token.value), depth=MutableDepth(depth))
                set_location(node, token)
                return node
            elif operation_type == "integer":
                node = AstIntegerConstant(value=int(token.value), depth=MutableDepth(depth))
                set_location(node, token)
                return node
        case _:
            raise NotImplementedError(token.value)
    raise NotImplementedError(token.value)

def operation_parser_float(
    stream: TokenStream, bolt_type: BoltType, argument_node: AstNode | None = None
) -> AstComputeRoot: 
    with float_syntax(stream):
        node = parse_expression(stream, "float", 0)
    root = AstComputeRoot(children=node, argument_node=argument_node, bolt_type=bolt_type, operation_type="float")
    set_location(root, node)
    return root

def operation_parser_integer(
    stream: TokenStream, bolt_type: BoltType, argument_node: AstNode | None = None
) -> AstComputeRoot:
    with integer_syntax(stream):
        node= parse_expression(stream, "integer", 0)
    root = AstComputeRoot(children=node, argument_node=argument_node, bolt_type=bolt_type, operation_type="integer")
    set_location(root, node)
    return root


def operation_parser(stream: TokenStream) -> AstComputeRoot:
    """Parse operation."""
    with stream.syntax(bolt=r"bolt_entity|bolt_block|bolt"):
        token = stream.expect("bolt")
        bolt_token_value = token.value
        BOLT_MAP: dict[str, BoltType] = {
            "bolt": "default",
            "bolt_entity": "entity",
            "bolt_block": "block",
        }
        bolt_type = BOLT_MAP[bolt_token_value]
        argument_node: AstNode | None = None
        match bolt_type:
            case "default":
                ...
            case "entity":
                argument_node = delegate("entity")(stream)
            case "block":
                argument_node = delegate("block_pos")(stream)
            case _:
                assert_never("BoltType", bolt_type)
    with stream.syntax(operation_type=r"float|integer"):
        operation_type: OperationType = stream.expect("operation_type").value  # pyright: ignore[reportAssignmentType]

    match operation_type:
        case "float":
            return operation_parser_float(stream, bolt_type, argument_node)
        case "integer":
            return operation_parser_integer(stream, bolt_type, argument_node)
    assert_never("OperationType", operation_type)
