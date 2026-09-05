import typing
from dataclasses import dataclass

from beet.core.utils import required_field
from bolt import AstFormatString, AstIdentifier
from mecha import AstChildren, AstNode

from bolt_compute.node import AstBaseInteger, AstBaseFloat


@dataclass(frozen=True, slots=True)
class AstIntegerNOP(AstBaseInteger):
    type = "bolt_compute_nop"
    children: AstBaseInteger = required_field()

    def serialize(self, result):
        yield self.children

@dataclass(frozen=True, slots=True)
class AstIntegerReference(AstBaseInteger):
    type = "reference"
    reference: str = required_field()

    def serialize(self, result):
        if self.depth.value != 0: result.append('"')
        result.append(self.reference)
        if self.depth.value != 0: result.append('"')

@dataclass(frozen=True, slots=True)
class AstIntegerBoltVariable(AstBaseFloat):
    type = "bolt_variable"
    value: AstIdentifier | AstFormatString = required_field()

    def serialize(self, result):
        if isinstance(self.value, (int)):
            yield AstIntegerConstant(value=self.value, depth=self.depth)
        elif isinstance(self.value, str):
            yield AstIntegerReference(reference=self.value, depth=self.depth)
        else:
            raise BaseException(self.__class__.__name__, self.value, type(self.value))


@dataclass(frozen=True, slots=True)
class AstIntegerBinomial(AstBaseInteger):
    type = "binomial"
    n: AstBaseInteger = required_field()
    p: AstBaseFloat = required_field()

    def serialize(self, result):
        result.append('{type:"minecraft:binomial",n:')
        yield self.n
        result.append(',p:')
        yield self.p
        result.append('}')


@dataclass(frozen=True, slots=True)
class AstIntegerConditional(AstBaseInteger):
    type = "conditional"
    condition: AstNode = required_field()
    on_true: AstBaseInteger = required_field()
    on_false: AstBaseInteger = required_field()


@dataclass(frozen=True, slots=True)
class AstBaseIntegerInput(AstBaseInteger):
    input: AstBaseInteger = required_field()


@dataclass(frozen=True, slots=True)
class AstIntegerAbs(AstBaseIntegerInput):
    type = "abs"


@dataclass(frozen=True, slots=True)
class AstBaseIntegerInputs(AstBaseInteger):
    inputs: list[AstBaseInteger] = required_field()


@dataclass(frozen=True, slots=True)
class AstIntegerAvg(AstBaseIntegerInputs):
    type = "avg"


@dataclass(frozen=True, slots=True)
class AstBaseIntegerBinaryOp(AstBaseInteger):
    left: AstBaseInteger = required_field()
    right: AstBaseInteger = required_field()

    def serialize(self, result):
        result.append('{type:"minecraft:'+self.type+'",left:')
        yield self.left
        result.append(',right:')
        yield self.left
        result.append('}')

@dataclass(frozen=True, slots=True)
class AstIntegerSub(AstBaseIntegerBinaryOp):
    type = "sub"


@dataclass(frozen=True, slots=True)
class AstIntegerDiv(AstBaseIntegerBinaryOp):
    type = "div"


@dataclass(frozen=True, slots=True)
class AstIntegerFloorDiv(AstBaseIntegerBinaryOp):
    type = "floor_div"


@dataclass(frozen=True, slots=True)
class AstIntegerMod(AstBaseIntegerBinaryOp):
    type = "mod"


@dataclass(frozen=True, slots=True)
class AstIntegerFloorMod(AstBaseIntegerBinaryOp):
    type = "floor_mod"


@dataclass(frozen=True, slots=True)
class AstIntegerPow(AstBaseIntegerBinaryOp):
    type = "pow"


@dataclass(frozen=True, slots=True)
class AstIntegerConstant(AstBaseInteger):
    type = "constant"
    value: int = required_field()

    def serialize(self, result):
        if self.depth.value == 0:
            result.append('{type:"minecraft:constant",value:')
            result.append(str(self.value))
            result.append('}')
        else:
            result.append(str(self.value))


@dataclass(frozen=True, slots=True)
class AstIntegerMin(AstBaseIntegerInputs):
    type = "min"


@dataclass(frozen=True, slots=True)
class AstIntegerMax(AstBaseIntegerInputs):
    type = "max"


@dataclass(frozen=True, slots=True)
class AstIntegerMul(AstBaseIntegerInputs):
    type = "mul"


@dataclass(frozen=True, slots=True)
class AstIntegerAdd(AstBaseIntegerInputs):
    type = "add"


@dataclass(frozen=True, slots=True)
class AstIntegerNegate(AstBaseIntegerInput):
    type = "negate"


@dataclass(frozen=True, slots=True)
class AstIntegerFromFloat(AstBaseInteger):
    type = "from_float"
    input: AstBaseFloat = required_field()


@dataclass(frozen=True, slots=True)
class AstBaseIntegerRange(AstBaseInteger):
    min: AstBaseInteger = required_field()
    max: AstBaseInteger = required_field()


@dataclass(frozen=True, slots=True)
class AstIntegerUniform(AstBaseIntegerRange):
    type = "uniform"


@dataclass(frozen=True, slots=True)
class AstIntegerWeightedListEntry(AstNode):
    data: AstBaseInteger = required_field()
    weight: int = required_field()


@dataclass(frozen=True, slots=True)
class AstIntegerWeightedList(AstBaseInteger):
    type = "weighted_list"
    distribution: AstChildren[AstIntegerWeightedListEntry] = required_field()


@dataclass(frozen=True, slots=True)
class AstIntegerScore(AstBaseInteger):
    type = "score"
    score: str = required_field()
    target: str = required_field()
    fallback: AstBaseInteger = required_field()


@dataclass(frozen=True, slots=True)
class AstIntegerStorage(AstBaseInteger):
    type = "storage"
    storage: str = required_field()
    path: str = required_field()
    fallback: AstBaseInteger = required_field()


@dataclass(frozen=True, slots=True)
class AstIntegerEnvironmentAttribute(AstBaseInteger):
    type = "environment_attribute"
    attribute: str = required_field()


@dataclass(frozen=True, slots=True)
class AstBaseIntegerNumberDispatcherCase:
    condition: AstNode = required_field()
    value: AstBaseInteger = required_field()


@dataclass(frozen=True, slots=True)
class AstIntegerNumberDispatcher(AstBaseInteger):
    type = "number_dispatcher"
    cases: list[AstBaseIntegerNumberDispatcherCase] = required_field()
    default: AstBaseInteger = required_field()
