from collections import deque
from dataclasses import dataclass, field
from typing import Iterable, Literal, Optional, Self

from beet.core.utils import required_field
from bolt import AstExpression, AstFormatString, AstIdentifier
from mecha import AstChildren, AstNbt, AstNbtPath, AstNode, AstObjective, AstOption, AstPlayerName, AstResourceLocation, AstUUID

from bolt_compute.float import AstFloatBoltVariable, AstFloatReference, AstFloatStorage
from bolt_compute.node import AstBaseInteger, AstBaseFloat, AstNodeContainer

from tokenstream import InvalidSyntax, set_location

@dataclass(frozen=True, slots=True)
class AstIntegerNOP(AstBaseInteger):
    type = "bolt_compute_nop"
    children: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})

    def serialize(self, result):
        yield self.children

@dataclass(frozen=True, slots=True)
class AstIntegerReference(AstBaseInteger):
    type = "reference"
    reference: AstResourceLocation = required_field(metadata={"bolt_compute_serialize": True})

    def serialize(self: Self, result: list[str]) -> Iterable[AstNode] | None:
        return AstFloatReference.serialize(self, result) # pyright: ignore[reportArgumentType]

@dataclass(frozen=True, slots=True)
class AstIntegerBoltVariable(AstBaseFloat):
    type = "bolt_variable"
    value: AstIdentifier | AstFormatString = required_field(metadata={"bolt_compute_serialize": True})

    def serialize(self, result):
        yield from AstFloatBoltVariable.serialize(self, result) # pyright: ignore[reportArgumentType]
@dataclass(frozen=True, slots=True)
class AstIntegerBinomial(AstBaseInteger):
    type = "binomial"
    n: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})
    p: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstIntegerConditional(AstBaseInteger):
    type = "conditional"
    condition: AstNbt | AstResourceLocation = required_field(metadata={"bolt_compute_serialize": True})
    on_true: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})
    on_false: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstBaseIntegerInput(AstBaseInteger):
    input: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstIntegerAbs(AstBaseIntegerInput):
    type = "abs"


@dataclass(frozen=True, slots=True)
class AstBaseIntegerInputs(AstBaseInteger):
    inputs: AstChildren[AstBaseInteger] = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstIntegerAvg(AstBaseIntegerInputs):
    type = "avg"


@dataclass(frozen=True, slots=True)
class AstBaseIntegerBinaryOp(AstBaseInteger):
    left: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})
    right: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})

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
    value: int = required_field(metadata={"bolt_compute_serialize": True})

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
    input: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstBaseIntegerRange(AstBaseInteger):
    min: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})
    max: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstIntegerUniform(AstBaseIntegerRange):
    type = "uniform"


@dataclass(frozen=True, slots=True)
class AstIntegerWeightedListEntry(AstNode):
    data: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})
    weight: int = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstIntegerWeightedList(AstBaseInteger):
    type = "weighted_list"
    distribution: AstChildren[AstIntegerWeightedListEntry] = required_field(metadata={"bolt_compute_serialize": True})

@dataclass(frozen=True, slots=True)
class AstTargetType(AstOption):
    parser = "bolt_compute_ast_target_type"
    options = {"this", "attacker", "direct_attacker", "attacking_player", "target_entity", "interacting_entity"}

@dataclass(frozen=True, slots=True)
class AstTargetTypeType(AstOption):
    parser = "bolt_compute_ast_target_type_type"
    options = {"context", "fixed"}


@dataclass(frozen=True, slots=True)
class AstIntegerScore(AstBaseInteger):
    _disable_function_call = True
    type = "score"
    target_type: AstTargetTypeType = required_field(metadata={"bolt_compute_serialize": True})
    target_target: Optional[AstTargetType] = field(default=None, metadata={"bolt_compute_serialize": True})
    target_name: Optional[AstPlayerName|AstUUID] = field(default=None, metadata={"bolt_compute_serialize": True})
    score: AstObjective = required_field(metadata={"bolt_compute_serialize": True})
    fallback: Optional[AstBaseInteger] = required_field(metadata={"bolt_compute_serialize": True})

    def serialize(self, result):
        result.append('{type:"minecraft:score"')
        result.append(',target:{')
        result.append('type:"')
        yield self.target_type
        result.append('"')
        if self.target_target:
            result.append(',target:"')
            yield self.target_target
            result.append('"')
        if self.target_name:
            result.append(',name:"')
            yield self.target_name
            result.append('"')

        result.append('}')
        result.append(',score:"')
        yield self.score
        result.append('"')
        if self.fallback:
            result.append(',fallback:')
            yield self.fallback
        result.append('}')


@dataclass(frozen=True, slots=True)
class AstIntegerScoreResolveLater(AstBaseInteger):
    type = "bolt_compute_score_resolve_later"
    args: AstChildren[AstNodeContainer] = required_field()

    def serialize(self, result):
        arr = deque([x.value for x in self.args])
        first = arr.popleft()
        if first in AstTargetType.options:
            target_type = AstTargetTypeType.from_value("context")
            target_target = AstTargetType.from_value(first)
            target_name = None
            score = AstObjective.from_value(arr.popleft())
        elif first in AstTargetTypeType.options:
            target_type = AstTargetTypeType.from_value(first)
            target_target = None
            name = arr.popleft()
            try:
                target_name = AstPlayerName.from_value(name)
            except ValueError:
                target_name = AstUUID.from_value(name)
            score = AstObjective.from_value(arr.popleft())
        else:
            exc = InvalidSyntax(f"{first} is not in {AstTargetType.options} or {AstTargetTypeType.options}")
            set_location(exc, self)
            raise exc
        
        fallback = None
        if len(arr) > 0:
            fallback = arr.popleft()
        
        if isinstance(fallback, str):
            fallback = AstIntegerReference(reference=AstResourceLocation.from_value(fallback), depth=self.depth)
        elif isinstance(fallback, int):
            fallback = AstIntegerConstant(value=fallback, depth=self.depth)
        elif fallback is None:
            ...
        else:
            raise NotImplementedError(fallback)

        if len(arr) > 0:
            exc = InvalidSyntax(f"Too many argument for the score literal, {arr} are left, {self}")
            set_location(exc, self)
            raise exc
        
        node = AstIntegerScore(target_type=target_type, target_target=target_target, target_name=target_name, score=score, fallback=fallback, depth=self.depth)
        set_location(node, self)
        yield node





@dataclass(frozen=True, slots=True)
class AstIntegerStorage(AstBaseInteger):
    type = "storage"
    storage: AstResourceLocation = required_field(metadata={"bolt_compute_serialize": True})
    path: AstNbtPath = required_field(metadata={"bolt_compute_serialize": True})
    fallback: Optional[AstBaseInteger] = field(default=None, metadata={"bolt_compute_serialize": True})




@dataclass(frozen=True, slots=True)
class AstIntegerEnvironmentAttribute(AstBaseInteger):
    type = "environment_attribute"
    attribute: str = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstBaseIntegerNumberDispatcherCase(AstNode):
    condition: AstNode = required_field(metadata={"bolt_compute_serialize": True})
    value: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstIntegerNumberDispatcher(AstBaseInteger):
    type = "number_dispatcher"
    cases: AstChildren[AstBaseIntegerNumberDispatcherCase] = required_field(metadata={"bolt_compute_serialize": True})
    default: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})
