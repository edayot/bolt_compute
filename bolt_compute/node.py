from dataclasses import dataclass
from typing import ClassVar, Literal, Optional, TypeIs

from beet.core.utils import required_field
from mecha import AstNode

from bolt_compute.types import BoltType


@dataclass
class MutableDepth:
    value: int

@dataclass(frozen=True, slots=True)
class AstComputeRoot(AstNode):
    children: AstBaseNode = required_field()
    argument_node: Optional[AstNode] = required_field()
    bolt_type: BoltType = required_field()
    operation_type: Literal["float", "integer"] = required_field()


@dataclass(frozen=True, slots=True)
class AstBaseNode(AstNode):
    type: ClassVar[str]
    value_type: ClassVar[Literal["integer", "float"]]
    depth: MutableDepth = required_field()

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

