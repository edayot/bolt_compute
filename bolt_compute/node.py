from dataclasses import dataclass
from typing import ClassVar, Generator, Iterable, Literal, Optional, Self, TypeIs, overload

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
        yield self.children

@dataclass(frozen=True, slots=True)
class AstBaseNode(AstNode):
    type: ClassVar[str]
    value_type: ClassVar[Literal["integer", "float"]]
    depth: MutableDepth = required_field()

    def serialize(self: Self, result: list[str]) -> Iterable[AstNode] | None:
        raise NotImplementedError(self.__class__.__name__)

    def cast_float(self) -> AstBaseFloat:
        assert self.value_type == "float"
        return self # pyright: ignore[reportReturnType]

    def cast_int(self) -> AstBaseInteger:
        assert self.value_type == "integer"
        return self # pyright: ignore[reportReturnType]
    


@dataclass(frozen=True, slots=True)
class AstBaseInteger(AstBaseNode):
    value_type = "integer"


@dataclass(frozen=True, slots=True)
class AstBaseFloat(AstBaseNode):
    value_type = "float"



@rule(AstComputeRoot, AstBaseNode)
def serialize_node(node: AstComputeRoot | AstBaseNode, result: list[str]) -> Iterable[AstNode] | None:
    if inspect.isgeneratorfunction(node.serialize):
        yield from node.serialize(result)
    else:
        return node.serialize(result)