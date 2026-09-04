import typing
from dataclasses import dataclass

from beet.core.utils import required_field
from mecha import AstNode

from bolt_compute.node import AstBaseInteger, AstBaseFloat


@dataclass(frozen=True, slots=True)
class AstBaseFloatInput(AstBaseFloat):
    input: AstBaseFloat = required_field()


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
    input: AstBaseInteger = required_field()


@dataclass(frozen=True, slots=True)
class AstBaseFloatInputs(AstBaseFloat):
    inputs: list[AstBaseFloat] = required_field()


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
class AstBaseFloatBinaryOp(AstBaseFloat):
    left: AstBaseFloat = required_field()
    right: AstBaseFloat = required_field()


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
class AstFloatPow(AstBaseFloatBinaryOp):
    type = "pow"


@dataclass(frozen=True, slots=True)
class AstBaseFloatConstant(AstBaseFloat):
    value: float = required_field()


@dataclass(frozen=True, slots=True)
class AstFloatConstant(AstBaseFloatConstant):
    type = "constant"


@dataclass(frozen=True, slots=True)
class AstBaseFloatRange(AstBaseFloat):
    min: AstBaseFloat = required_field()
    max: AstBaseFloat = required_field()


@dataclass(frozen=True, slots=True)
class AstFloatUniform(AstBaseFloatRange):
    type = "uniform"


@dataclass(frozen=True, slots=True)
class AstFloatWeightedListEntry:
    data: AstBaseFloat = required_field()
    weight: int = required_field()


@dataclass(frozen=True, slots=True)
class AstFloatWeightedList(AstBaseFloat):
    type = "weighted_list"
    distribution: list[AstFloatWeightedListEntry] = required_field()


@dataclass(frozen=True, slots=True)
class AstFloatStorage(AstBaseFloat):
    type = "storage"
    storage: str = required_field()
    path: str = required_field()
    fallback: AstBaseFloat = required_field()


@dataclass(frozen=True, slots=True)
class AstFloatEnvironmentAttribute(AstBaseFloat):
    type = "environment_attribute"
    attribute: str = required_field()


@dataclass(frozen=True, slots=True)
class AstBaseFloatNumberDispatcherCase:
    condition: AstNode = required_field()
    value: AstBaseFloat = required_field()


@dataclass(frozen=True, slots=True)
class AstFloatNumberDispatcher(AstBaseFloat):
    type = "number_dispatcher"
    cases: list[AstBaseFloatNumberDispatcherCase] = required_field()
    default: AstBaseFloat = required_field()


@dataclass(frozen=True, slots=True)
class AstFloatConditional(AstBaseFloat):
    type = "conditional"
    condition: AstNode = required_field()
    on_true: AstBaseFloat = required_field()
    on_false: AstBaseFloat = required_field()


@dataclass(frozen=True, slots=True)
class AstFloatEnchantmentLevel(AstBaseFloat):
    type = "enchantment_level"
    amount: AstNode = required_field()
