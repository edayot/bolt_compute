from dataclasses import dataclass
from typing import Any, ClassVar, Generator, Iterable, Literal, Optional, Self, Type, TypeIs, overload

from beet.core.utils import required_field
from mecha import AstNode, rule

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

@dataclass(frozen=True, slots=True)
class AstBaseNode(AstNode):
    type: ClassVar[str]
    value_type: ClassVar[Literal["integer", "float"]]
    depth: MutableDepth = required_field()

    def serialize(self: Self, result: list[str]) -> Iterable[AstNode] | None:
        source_file = inspect.getsourcefile(self.__class__)
        source_lines = inspect.getsourcelines(self.__class__)
        line_number = source_lines[1]
        
        raise NotImplementedError(
            f"{self.__class__.__name__}.serialize() - "
            f"Implement in {source_file}:{line_number}"
        )

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
        type = getattr(cls, "type", None)
        if type is not None and isinstance(type, str) and not type.startswith("bolt_compute_"):
            INTEGER_NODES[type] = cls
        return super().__init_subclass__()


@dataclass(frozen=True, slots=True)
class AstBaseFloat(AstBaseNode):
    value_type = "float"

    def __init_subclass__(cls) -> None:
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