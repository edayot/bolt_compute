from dataclasses import dataclass, fields
from types import MappingProxyType
from typing import Any, ClassVar, Generator, Iterable, Literal, Optional, Self, Type, TypeIs, overload

from beet.core.utils import required_field
from mecha import AstChildren, AstNbtPath, AstNode, AstResourceLocation, rule

from bolt_compute.types import BoltType
import inspect

@dataclass
class MutableDepth:
    value: int

@dataclass(frozen=True, slots=True)
class AstComputeRoot(AstNode):
    children: AstBaseNode = required_field()
    argument_node: Optional[AstNode] = required_field()
    bolt_type: BoltType = required_field()
    operation_type: Literal["float", "integer"] = required_field()

    def serialize(self: Self, result: list[str]) -> Iterable[AstNode] | None:
        result.append(self.bolt_type)
        result.append(" ")
        if self.argument_node is not None:
            yield self.argument_node
            result.append(" ")
        result.append(self.operation_type)
        result.append(" ")
        children_start_index = len(result)
        yield self.children
        children_last_index = len(result)
        children_computed = "".join(result[children_start_index:children_last_index])
        # children_computed coud be used in the future for data validation

def get_serializable_fields(instance) -> dict[str, MappingProxyType[Any, Any]]:
    """Get all fields with bolt_compute_serialize metadata as {name: type}"""
    return {
        f.name: f.metadata
        for f in fields(instance)
        if f.metadata.get("bolt_compute_serialize")
    }

@dataclass(frozen=True, slots=True)
class AstBaseNode(AstNode):
    type: ClassVar[str]
    value_type: ClassVar[Literal["integer", "float"]]
    depth: MutableDepth = required_field()
    _disable_function_call: ClassVar[bool] = False

    def serialize(self: Self, result: list[str]) -> Iterable[AstNode] | None:
        result.append('{type:"minecraft:')
        result.append(self.type)
        result.append('"')
        for field, metadata in get_serializable_fields(self).items():
            value = getattr(self, field)
            if value is None: continue
            result.append(',')
            result.append(field)
            result.append(':')
            if isinstance(value, AstResourceLocation):
                if self.depth.value == 0:
                    result.append(value.get_value())
                else:
                    result.append(repr(value.get_value()))
            elif isinstance(value, AstNbtPath):
                index_start = len(result)
                yield value
                index_end = len(result)
                node_value = "".join(result[index_start:index_end])
                while len(result) != index_start:
                    result.pop()
                result.append(repr(node_value))
            elif isinstance(value, AstNode):
                yield value
            elif isinstance(value, (float, int)):
                result.append(str(value))
            elif isinstance(value, AstChildren):
                result.append('[')
                for child in value:
                    yield child
                    result.append(',')
                result.append(']')
            else:
                raise NotImplementedError(field, type(value))
        result.append('}')



    def cast_float(self) -> AstBaseFloat:
        assert self.value_type == "float"
        return self # pyright: ignore[reportReturnType]

    def cast_int(self) -> AstBaseInteger:
        assert self.value_type == "integer"
        return self # pyright: ignore[reportReturnType]
    

INTEGER_NODES: dict[str, Type[AstBaseInteger]] = {}
FLOAT_NODES:   dict[str, Type[AstBaseFloat]] = {}


@dataclass(frozen=True, slots=True)
class AstBaseInteger(AstBaseNode):
    value_type = "integer"

    def __init_subclass__(cls) -> None:
        _disable_function_call = getattr(cls, "_disable_function_call", False)
        if not _disable_function_call:
            type = getattr(cls, "type", None)
            if type is not None and isinstance(type, str) and not type.startswith("bolt_compute_"):
                INTEGER_NODES[type] = cls
        return super().__init_subclass__()


@dataclass(frozen=True, slots=True)
class AstBaseFloat(AstBaseNode):
    value_type = "float"

    def __init_subclass__(cls) -> None:
        _disable_function_call = getattr(cls, "_disable_function_call", False)
        if not _disable_function_call:
            type = getattr(cls, "type", None)
            if type is not None and isinstance(type, str) and not type.startswith("bolt_compute_"):
                FLOAT_NODES[type] = cls
        return super().__init_subclass__()



@rule(AstComputeRoot, AstBaseNode)
def serialize_node(node: AstComputeRoot | AstBaseNode, result: list[str]) -> Iterable[AstNode] | None:
    if inspect.isgeneratorfunction(node.serialize):
        yield from node.serialize(result)
    else:
        return node.serialize(result)


DEFAULT_NODE_ARGS = ("self", "location", "end_location", "depth", "return", "type", "serialize", "cast_float", "cast_int", "parser")