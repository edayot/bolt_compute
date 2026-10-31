import inspect
import typing
from dataclasses import dataclass, field

from beet.core.utils import required_field
from bolt import AstFormatString, AstIdentifier
from mecha import AstChildren, AstNbt, AstNbtCompound, AstNbtList, AstNbtPath, AstNbtValue, AstNode, AstResourceLocation, Diagnostic, Mecha
from nbtlib import Float

from bolt_compute.node import AstBaseInteger, AstBaseFloat, nbt_string
from tokenstream import set_location


@dataclass(frozen=True, slots=True)
class AstFloatNOP(AstBaseFloat):
    type = "bolt_compute_nop"
    children: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})

    def to_nbt(self, mc: Mecha) -> AstNbt:
        return self.children.to_nbt(mc)


@dataclass(frozen=True, slots=True)
class AstFloatReference(AstBaseFloat):
    type = "bolt_compute_reference"
    reference: AstResourceLocation = required_field(metadata={"bolt_compute_serialize": True})

    def to_nbt(self, mc: Mecha) -> AstNbt:
        return nbt_string(self, self.reference.get_value())

@dataclass(frozen=True, slots=True)
class AstFloatBoltVariable(AstBaseFloat):
    type = "bolt_compute_variable"
    value: AstIdentifier | AstFormatString = required_field(metadata={"bolt_compute_serialize": True})

    def to_nbt(self, mc: Mecha) -> AstNbt:
        # bolt evaluates the variable before the transform step
        value: typing.Any = self.value
        if isinstance(value, (int, float)) and not isinstance(value, bool):
            node = AstFloatConstant(value=float(value))
        elif isinstance(value, str):
            node = AstFloatReference(reference=AstResourceLocation.from_value(value))
        else:
            raise set_location(Diagnostic("error", f"Expected a number or a number provider id but got {value!r}."), self)
        return set_location(node, self).to_nbt(mc)
    
@dataclass(frozen=True, slots=True)
class AstBaseFloatInput(AstBaseFloat):
    input: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstFloatAbs(AstBaseFloatInput):
    type = "abs"


@dataclass(frozen=True, slots=True)
class AstFloatCeil(AstBaseFloatInput):
    type = "ceil"


@dataclass(frozen=True, slots=True)
class AstFloatFloor(AstBaseFloatInput):
    type = "floor"


@dataclass(frozen=True, slots=True)
class AstFloatRound(AstBaseFloatInput):
    type = "round"


@dataclass(frozen=True, slots=True)
class AstFloatTruncate(AstBaseFloatInput):
    type = "truncate"


@dataclass(frozen=True, slots=True)
class AstFloatSqrt(AstBaseFloatInput):
    type = "sqrt"


@dataclass(frozen=True, slots=True)
class AstFloatSin(AstBaseFloatInput):
    type = "sin"


@dataclass(frozen=True, slots=True)
class AstFloatCos(AstBaseFloatInput):
    type = "cos"


@dataclass(frozen=True, slots=True)
class AstFloatNegate(AstBaseFloatInput):
    type = "negate"


@dataclass(frozen=True, slots=True)
class AstFloatFromInt(AstBaseFloat):
    type = "from_int"
    input: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstBaseFloatInputs(AstBaseFloat):
    inputs: AstChildren[AstBaseFloat] = required_field(metadata={"bolt_compute_serialize": True})



@dataclass(frozen=True, slots=True)
class AstFloatAvg(AstBaseFloatInputs):
    type = "avg"


@dataclass(frozen=True, slots=True)
class AstFloatMin(AstBaseFloatInputs):
    type = "min"


@dataclass(frozen=True, slots=True)
class AstFloatMax(AstBaseFloatInputs):
    type = "max"


@dataclass(frozen=True, slots=True)
class AstFloatMul(AstBaseFloatInputs):
    type = "mul"


@dataclass(frozen=True, slots=True)
class AstFloatAdd(AstBaseFloatInputs):
    type = "add"


@dataclass(frozen=True, slots=True)
class AstFloatLength(AstBaseFloatInputs):
    type = "length"

@dataclass(frozen=True, slots=True)
class AstFloatPow(AstBaseFloat):
    type = "pow"
    base: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})
    exponent: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})
@dataclass(frozen=True, slots=True)
class AstBaseFloatBinaryOp(AstBaseFloat):
    left: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})
    right: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstFloatSub(AstBaseFloatBinaryOp):
    type = "sub"


@dataclass(frozen=True, slots=True)
class AstFloatDiv(AstBaseFloatBinaryOp):
    type = "div"


@dataclass(frozen=True, slots=True)
class AstFloatMod(AstBaseFloatBinaryOp):
    type = "mod"

@dataclass(frozen=True, slots=True)
class AstBaseFloatConstant(AstBaseFloat):
    value: float = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstFloatConstant(AstBaseFloatConstant):
    type = "constant"

    def to_nbt(self, mc: Mecha) -> AstNbt:
        return set_location(AstNbtValue(value=Float(self.value)), self)


@dataclass(frozen=True, slots=True)
class AstBaseFloatRange(AstBaseFloat):
    min: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})
    max: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstFloatUniform(AstBaseFloatRange):
    type = "uniform"


@dataclass(frozen=True, slots=True)
class AstFloatWeightedListEntry(AstNode):
    data: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})
    weight: int = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstFloatWeightedList(AstBaseFloat):
    type = "weighted_list"
    distribution: AstChildren[AstFloatWeightedListEntry] = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstFloatStorage(AstBaseFloat):
    type = "storage"
    storage: AstResourceLocation = required_field(metadata={"bolt_compute_serialize": True})
    path: AstNbtPath = required_field(metadata={"bolt_compute_serialize": True})
    fallback: typing.Optional[AstBaseFloat] = field(default=None, metadata={"bolt_compute_serialize": True})

@dataclass(frozen=True, slots=True)
class AstFloatEnvironmentAttribute(AstBaseFloat):
    type = "environment_attribute"
    attribute: str = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstBaseFloatNumberDispatcherCase(AstNode):
    condition: AstNode = required_field(metadata={"bolt_compute_serialize": True})
    value: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstFloatNumberDispatcher(AstBaseFloat):
    type = "number_dispatcher"
    cases: AstChildren[AstBaseFloatNumberDispatcherCase] =required_field(metadata={"bolt_compute_serialize": True})
    default: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstFloatConditional(AstBaseFloat):
    type = "conditional"
    condition: AstResourceLocation | AstNbtCompound | AstNbtList = required_field(metadata={"bolt_compute_serialize": True})
    on_true: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})
    on_false: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})

@dataclass(frozen=True, slots=True)
class AstFloatEnchantmentLevel(AstBaseFloat):
    type = "enchantment_level"
    amount: AstNode = required_field(metadata={"bolt_compute_serialize": True})
