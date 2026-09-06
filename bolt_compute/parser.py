from dataclasses import MISSING, Field, fields
from types import NoneType
from typing import Any, Literal, Type, TypeIs, Union, assert_never, cast, get_args, overload, reveal_type

from bolt import AstCall, AstFormatString, AstIdentifier, AstValue
from mecha import (
    AstNode,
    UnrecognizedParser,
    delegate,
)
from tokenstream import InvalidSyntax, Token, TokenStream, set_location

from bolt_compute.node import DEFAULT_NODE_ARGS, AstBaseNode, AstComputeRoot, MutableDepth, FLOAT_NODES, INTEGER_NODES
from bolt_compute.float import *
from bolt_compute.integer import *
from bolt_compute.types import AdditiveOperation, BoltType, MultiplicativeOperation, Operation, OperationType
from contextlib import contextmanager
from collections import deque



FUNCTIONS = (
    "abs",
    "avg",
)

@contextmanager
def integer_syntax(stream: TokenStream):
    with stream.syntax(
        oparent=r"\(",
        cparent=r"\)",
        conditional=r"if|else",
        additive=r"\+|\-",
        multiplicative=r'\*\*' r'|\*' r'|\/\/' r'|\%',
        number=r"[+-]?[0-9]+",
        quotes=r'"|\'',
        call='|'.join([x + r'\(' for x in INTEGER_NODES.keys()]),
        storage=r"storage",
        score=r"score",
    ):
        with stream.provide(bolt_compute_keywords={x: None for x in ["conditional", "storage", "score", "call"]}):
            yield

@contextmanager
def float_syntax(stream: TokenStream):
    with stream.syntax(
        oparent=r"\(",
        cparent=r"\)",
        conditional=r"if|else",
        additive=r"\+|\-",
        multiplicative=r'\*\*' r'|\*' r'|\/' r'|\%',
        number=r"[+-]?([0-9]*[.])?[0-9]+",
        quotes=r'"|\'',
        call='|'.join([x + r'\(' for x in FLOAT_NODES.keys()]),
        storage=r"storage",
        score=r"score",
    ):
        with stream.provide(bolt_compute_keywords={x: None for x in ["conditional", "storage", "score", "call"]}):
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
                    node = AstFloatReference(reference=AstResourceLocation.from_value(bolt_node.value), depth=MutableDepth(depth))
                    set_location(node, bolt_node)
                    return node
                elif operation_type == "integer":
                    commit()
                    node = AstIntegerReference(reference=AstResourceLocation.from_value(bolt_node.value), depth=MutableDepth(depth))
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

    token = stream.expect_any("number", "quotes", "storage", "score", "additive", "call")
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
        case Token("additive"):
            if token.value == "+":
                if operation_type == "integer":
                    t = AstIntegerNOP
                else: 
                    t = AstFloatNOP
                node = t(children=parse_primary(stream, operation_type, depth+1))
            else:
                if operation_type == "integer":
                    t = AstIntegerNegate
                else:
                    t = AstFloatNegate
                node = t(input=parse_primary(stream, operation_type, depth+1), depth=MutableDepth(depth))
            set_location(node, token)
            return node
        case Token("storage"):
            storage = parse_node_or_union(stream, operation_type, {"type": AstResourceLocation, "required": True}, depth+1)
            path = parse_node_or_union(stream, operation_type, {"type": AstNbtPath, "required": True}, depth+1)
            if operation_type == "float":
                fallback = parse_node_or_union(stream, operation_type, {"type": Union[AstBaseFloat | None], "required": False, "has_default": True, "default": None}, depth+1)
                node = AstFloatStorage(storage=storage, path=path, fallback=fallback, depth=MutableDepth(depth))
            else:
                fallback = parse_node_or_union(stream, operation_type, {"type": Union[AstBaseInteger | None], "required": False, "has_default": True, "default": None}, depth+1)
                node = AstFloatStorage(storage=storage, path=path, fallback=fallback, depth=MutableDepth(depth))
            set_location(node, token)
            return node
        case Token("score"):
            score = parse_node_or_union(stream, operation_type, {"type": AstResourceLocation, "required": True}, depth+1)
            target = parse_node_or_union(stream, operation_type, {"type": AstNbtPath, "required": True}, depth+1)
            fallback = parse_node_or_union(stream, operation_type, {"type": Union[AstBaseInteger | None], "required": False, "has_default": True, "default": None}, depth+1)
            node = AstFloatStorage(storage=storage, path=path, fallback=fallback, depth=MutableDepth(depth))
            set_location(node, token)
            return node

        case Token("call"):
            call_value = token.value[:-1]
            if operation_type == "float":
                cls = FLOAT_NODES[call_value]
                input_cls = AstBaseFloatInput
                inputs_cls = AstBaseFloatInputs
            elif operation_type == "integer":
                cls = INTEGER_NODES[call_value]
                input_cls = AstBaseFloatInput
                inputs_cls = AstBaseFloatInputs
            else:
                assert_never(operation_type)
            with stream.syntax(
                argument=r'[a-z]+=',
                comma=r','
            ):
                # they are 2 option, named args and unamed args
                if issubclass(cls, input_cls):
                    with stream.checkpoint() as commit:
                        stream.expect(("argument", "input="))
                        node = cls(input=parse_expression(stream, operation_type, depth+1), depth=MutableDepth(depth))
                        stream.expect("cparent")
                        set_location(node, token)
                        commit()
                        return node
                    node = cls(input=parse_expression(stream, operation_type, depth+1), depth=MutableDepth(depth))
                    stream.expect("cparent")
                    set_location(node, token)
                    return node
                elif issubclass(cls, inputs_cls):
                    with stream.checkpoint() as commit:
                        stream.expect(("argument", "inputs="))
                        node = cls(inputs=parse_list(stream, operation_type, depth+1), depth=MutableDepth(depth))
                        stream.expect("cparent")
                        set_location(node, token)
                        commit()
                        return node
                    with stream.checkpoint() as commit:
                        node = cls(inputs=parse_list(stream, operation_type, depth+1), depth=MutableDepth(depth))
                        stream.expect("cparent")
                        set_location(node, token)
                        commit()
                        return node
                    node = cls(inputs=parse_star_arguments(stream, operation_type, depth+1), depth=MutableDepth(depth))
                    set_location(node, token)
                    return node
                else:
                    node = parse_function_call(cls, stream, token, operation_type, depth)
                    set_location(node, token)
                    return node
                    
                raise NotImplementedError(cls.__name__, cls.type)

            raise NotImplementedError()
        case _:
            raise NotImplementedError(token.type)
    raise NotImplementedError(token.type)


def parse_function_call(cls: type[AstBaseFloat] | type[AstBaseInteger], stream: TokenStream, token: Token, operation_type: OperationType, depth: int):
    """Parse function call with named arguments based on signature"""
    
    sig = inspect.signature(cls.__init__)
    field_dict = {f.name: f for f in fields(cls)}
    args = {}
    
    for param_name, param in sig.parameters.items():
        if param_name in DEFAULT_NODE_ARGS:
            continue
        
        annotation = param.annotation if param.annotation != inspect.Parameter.empty else None
        has_default = param.default != inspect.Parameter.empty
        default_value = param.default if has_default else None

        # Get the default_factory from dataclass field
        default_factory = None
        has_default_factory = False
        if param_name in field_dict:
            field_obj = field_dict[param_name]
            if field_obj.default_factory is not MISSING:
                default_factory = field_obj.default_factory
                has_default_factory = True
                has_default = False
                from beet.core.utils import _raise_required_field
                if default_factory is _raise_required_field:
                    has_default = False
                    has_default_factory = False
        
        args[param_name] = {
            "type": annotation,
            "default": default_value,
            "required": not(has_default or has_default_factory),
            "has_default": has_default,
            "default_factory": default_factory,
            "has_default_factory": has_default_factory,
        }
    args_queue = deque(args.items())
        
    with stream.checkpoint() as commit:
        parsed_arguments: dict[str, Any] = {}
        
        while len(args) > 0:
            arg = stream.expect("argument")
            arg_name = arg.value[:-1]
            commit()
            
            if arg_name not in args:
                expected = ", ".join(repr(x) for x in args.keys())
                exc = InvalidSyntax(
                    f"Expected {expected} but got {repr(arg_name)} argument of function {token.value}"
                )
                set_location(exc, arg)
                raise exc
            
            node = parse_node_or_union(stream, operation_type, args[arg_name], depth)
            if isinstance(node, AstNode):
                set_location(node, arg)
            parsed_arguments[arg_name] = node
            args.pop(arg_name)
            
            if len(args) > 0:
                stream.expect("comma")
            else:
                # optional comma at the end
                with stream.checkpoint() as c:
                    stream.expect("comma")
                    c()
        
        node = cls(**parsed_arguments, depth=MutableDepth(depth)) # pyright: ignore[reportArgumentType]
        stream.expect("cparent")
        set_location(node, token)
        commit()
        return node
    
    parsed_arguments = {}
    number_of_arguments_required = len([x for x in args_queue if x[1]["required"]])
    while len(args_queue) > 0:
        arg = args_queue.popleft()
        with stream.syntax(
            argument=None,
        ):
            node = parse_node_or_union(stream, operation_type, arg[1], depth)
            if isinstance(node, AstNode):
                set_location(node, arg)
        parsed_arguments[arg[0]] = node
        if len(args_queue)>0:
            with stream.checkpoint() as commit:
                stream.expect("comma")
                commit()
                continue
            # comma are optional if and only if there is only argument with default values left
            if not all(not x[1]["required"] for x in args_queue):
                missing = ", ".join((repr(x[0]) for x in args_queue if x[1]["required"]))
                number_of_arguments = len([x for x in args_queue if x[1]["required"]])

                exc = InvalidSyntax(
                    f"Not enought arguments expected {number_of_arguments_required} arguments but got {number_of_arguments} in function {token.value}, missing {missing}"
                )
                set_location(exc, token)
                raise exc
            # all parameters left have default values
            while len(args_queue) > 0:
                arg = args_queue.popleft()
                parsed_arguments[arg[0]] = arg[1]["default"] if arg[1]["has_default"] else arg[1]["default_factory"]()
        else:
            # optional comma at the end
            with stream.checkpoint() as c:
                stream.expect("comma")
                c()
    node = cls(**parsed_arguments, depth=MutableDepth(depth))
    stream.expect("cparent")
    set_location(node, token)
    return node



def parse_node_or_union(stream: TokenStream, operation_type: OperationType, node_or_union: Any, depth: int):
    if isinstance(node_or_union["type"], Union):
        for arg in get_args(node_or_union["type"]):
            with stream.checkpoint() as commit:
                node = parse_node_or_union(stream, operation_type, {"type":arg, "required": True}, depth)
                commit()
                return node
        if not node_or_union["required"]:
            return node_or_union["default"] if node_or_union["has_default"] else node_or_union["default_factory"]()
        raise InvalidSyntax("No successfull union detected")
    elif issubclass(node_or_union["type"], AstBaseInteger):
        with integer_syntax(stream):
            return parse_expression(stream, "integer", depth + 1)
    elif issubclass(node_or_union["type"], AstBaseFloat):
        with float_syntax(stream):
            return parse_expression(stream, "float", depth + 1)
    elif hasattr(node_or_union["type"], 'parser') and node_or_union["type"].parser:
        return delegate(node_or_union["type"].parser)(stream)
    elif issubclass(node_or_union["type"], NoneType):
        raise InvalidSyntax("None is not representable as a Literal")
    else:
        if not node_or_union["required"]:
            return node_or_union["default"] if node_or_union["has_default"] else node_or_union["default_factory"]()
        raise NotImplementedError(node_or_union)
    raise NotImplementedError(node_or_union)





@overload
def parse_list(stream: TokenStream, operation_type: Literal["float"], depth: int) -> AstChildren[AstBaseFloat]: ...
@overload
def parse_list(stream: TokenStream, operation_type: Literal["integer"], depth: int) -> AstChildren[AstBaseInteger]: ...
def parse_list(stream: TokenStream, operation_type: OperationType, depth: int) -> AstChildren[AstNode]:
    """Parse a comma-separated list of expressions inside brackets."""
    with stream.syntax(
        obracket=r'\[',
        cbracket=r'\]',
    ):
        stream.expect("obracket")
        values: list[AstNode] = []
        while True:
            with stream.checkpoint() as commit:
                stream.expect("cbracket")
                commit()
                break
            values.append(parse_expression(stream, operation_type, depth=depth + 1))
            follow = stream.expect_any("comma", "cbracket")
            match follow:
                case Token("cbracket"):
                    break
                case Token("comma"):
                    ...
    return AstChildren(values)


@overload
def parse_star_arguments(stream: TokenStream, operation_type: Literal["float"], depth: int) -> AstChildren[AstBaseFloat]: ...
@overload
def parse_star_arguments(stream: TokenStream, operation_type: Literal["integer"], depth: int) -> AstChildren[AstBaseInteger]: ...
def parse_star_arguments(stream: TokenStream, operation_type: OperationType, depth: int) -> AstChildren[AstNode]:
    """Parse a comma-separated list of expressions until cparent."""
    values: list[AstNode] = []
    while True:
        with stream.checkpoint() as commit:
            stream.expect("cparent")
            commit()
            break
        values.append(parse_expression(stream, operation_type, depth=depth + 1))
        follow = stream.expect_any("comma", "cparent")
        match follow:
            case Token("cparent"):
                break
            case Token("comma"):
                ...
    return AstChildren(values)


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
