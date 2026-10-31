from dataclasses import dataclass, fields
from types import MappingProxyType
from typing import Any, ClassVar, Literal, Optional, Type

from beet.core.utils import required_field
from mecha import (
    AstChildren,
    AstNbt,
    AstNbtCompound,
    AstNbtCompoundEntry,
    AstNbtCompoundKey,
    AstNbtList,
    AstNbtValue,
    AstNode,
    AstResourceLocation,
    Mecha,
)
from nbtlib import String
from tokenstream import set_location

from bolt_compute.types import BoltType

@dataclass(frozen=True, slots=True)
class AstComputeRoot(AstNode):
    children: AstBaseNode = required_field()
    argument_node: Optional[AstNode] = required_field()
    bolt_type: BoltType = required_field()
    operation_type: Literal["float", "integer"] = required_field()

def get_serializable_fields(instance) -> dict[str, MappingProxyType[Any, Any]]:
    """Get all fields with bolt_compute_serialize metadata as {name: type}"""
    return {
        f.name: f.metadata
        for f in fields(instance)
        if f.metadata.get("bolt_compute_serialize")
    }


def nbt_string(node: AstNode, value: str) -> AstNbtValue:
    return set_location(AstNbtValue(value=String(value)), node)


def nbt_compound(node: AstNode, entries: dict[str, AstNbt]) -> AstNbtCompound:
    compound = AstNbtCompound(
        entries=AstChildren(
            AstNbtCompoundEntry(key=AstNbtCompoundKey(value=key), value=value)
            for key, value in entries.items()
        )
    )
    return set_location(compound, node)


def fields_to_nbt(node: AstNode, mc: Mecha) -> dict[str, AstNbt]:
    """Convert every field with bolt_compute_serialize metadata, skipping None values"""
    return {
        name: field_to_nbt(value, mc)
        for name in get_serializable_fields(node)
        if (value := getattr(node, name)) is not None
    }


def field_to_nbt(value: Any, mc: Mecha) -> AstNbt:
    if isinstance(value, AstBaseNode):
        return value.to_nbt(mc)
    elif isinstance(value, AstNbt):
        return value
    elif isinstance(value, AstResourceLocation):
        return nbt_string(value, value.get_value())
    elif isinstance(value, (AstChildren, list)):
        return AstNbtList(elements=AstChildren(field_to_nbt(child, mc) for child in value))
    elif isinstance(value, AstNode) and get_serializable_fields(value):
        return nbt_compound(value, fields_to_nbt(value, mc))
    elif isinstance(value, AstNode):
        return nbt_string(value, mc.serialize(value))
    elif isinstance(value, (int, float, str)):
        return AstNbt.from_value(value)
    raise NotImplementedError(type(value))


@dataclass(frozen=True, slots=True)
class AstBaseNode(AstNode):
    type: ClassVar[str]
    value_type: ClassVar[Literal["integer", "float"]]
    _disable_function_call: ClassVar[bool] = False

    def to_nbt(self, mc: Mecha) -> AstNbt:
        """Convert the node to its nbt representation when nested in another number provider"""
        return nbt_compound(self, {
            "type": nbt_string(self, f"minecraft:{self.type}"),
            **fields_to_nbt(self, mc),
        })

    def to_provider(self, mc: Mecha) -> AstNbt | AstResourceLocation:
        """Convert the node to a valid top-level number provider argument"""
        nbt = self.to_nbt(mc)
        if not isinstance(nbt, AstNbtValue):
            return nbt
        if isinstance(nbt.value, String):
            return set_location(AstResourceLocation.from_value(str(nbt.value)), nbt)
        return nbt_compound(nbt, {
            "type": nbt_string(nbt, "minecraft:constant"),
            "value": nbt,
        })

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


@dataclass(frozen=True, slots=True)
class AstNodeContainer(AstNode):
    value: AstNode = required_field()



DEFAULT_NODE_ARGS = ("self", "location", "end_location", "return", "type", "to_nbt", "to_provider", "cast_float", "cast_int", "parser")
