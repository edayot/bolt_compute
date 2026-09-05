import inspect
import typing
from dataclasses import dataclass

from beet.core.utils import required_field
from bolt import AstFormatString, AstIdentifier
from mecha import AstChildren, AstNode

from bolt_compute.node import AstBaseInteger, AstBaseFloat
from tokenstream import InvalidSyntax, set_location


@dataclass(frozen=True, slots=True)
class AstFloatNOP(AstBaseFloat):
    type = "bolt_compute_nop"
    children: AstBaseInteger = required_field()

    def serialize(self, result):
        yield self.children


@dataclass(frozen=True, slots=True)
class AstFloatReference(AstBaseFloat):
    type = "bolt_compute_reference"
    reference: str = required_field()

    def serialize(self, result):
        if self.depth.value != 0: result.append('"')
        result.append(self.reference)
        if self.depth.value != 0: result.append('"')

@dataclass(frozen=True, slots=True)
class AstFloatBoltVariable(AstBaseFloat):
    type = "bolt_compute_variable"
    value: AstIdentifier | AstFormatString = required_field()

    def serialize(self, result):
        if isinstance(self.value, (int, float)):
            yield AstFloatConstant(value=self.value, depth=self.depth)
        elif isinstance(self.value, str):
            yield AstFloatReference(reference=self.value, depth=self.depth)
        else:
            exc = InvalidSyntax(self.__class__.__name__, self.value, type(self.value))
            set_location(exc, self)
            raise exc
    
@dataclass(frozen=True, slots=True)
class AstBaseFloatInput(AstBaseFloat):
    input: AstBaseFloat = required_field()

    def serialize(self, result):
        result.append('{type:"minecraft:')
        result.append(self.type)
        result.append('",input:')
        yield self.input
        result.append('}')


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
    inputs: AstChildren[AstBaseFloat] = required_field()

    def serialize(self, result):
        result.append('{type:"minecraft:'+ self.type + '",inputs:[')
        for input in self.inputs:
            yield input
            result.append(",")
        result.append("]}")



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

    def serialize(self, result):
        result.append('{type:"minecraft:')
        result.append(self.type)
        result.append('",left:')
        yield self.left
        result.append(',right:')
        yield self.right
        result.append('}')


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

    def serialize(self, result):
        if self.depth.value == 0:
            result.append('{type:"minecraft:constant",value:')
            result.append(str(self.value))
            result.append('}')
        else:
            result.append(str(self.value))


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
class AstFloatWeightedListEntry(AstNode):
    data: AstBaseFloat = required_field()
    weight: int = required_field()


@dataclass(frozen=True, slots=True)
class AstFloatWeightedList(AstBaseFloat):
    type = "weighted_list"
    distribution: AstChildren[AstFloatWeightedListEntry] = required_field()


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
