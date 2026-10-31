from collections import deque
from dataclasses import dataclass, field
from typing import Any, Literal, Optional

from beet.core.utils import required_field
from bolt import AstExpression, AstFormatString, AstIdentifier
from mecha import AstChildren, AstNbt, AstNbtCompound, AstNbtList, AstNbtPath, AstNbtValue, AstNode, AstObjective, AstOption, AstPlayerName, AstResourceLocation, AstUUID, Diagnostic, Mecha
from nbtlib import Int

from bolt_compute.float import AstFloatReference, AstFloatStorage
from bolt_compute.node import AstBaseInteger, AstBaseFloat, AstNodeContainer, field_to_nbt, nbt_compound, nbt_string

from tokenstream import set_location

@dataclass(frozen=True, slots=True)
class AstIntegerNOP(AstBaseInteger):
    type = "bolt_compute_nop"
    children: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})

    def to_nbt(self, mc: Mecha) -> AstNbt:
        return self.children.to_nbt(mc)

@dataclass(frozen=True, slots=True)
class AstIntegerReference(AstBaseInteger):
    type = "bolt_compute_reference"
    reference: AstResourceLocation = required_field(metadata={"bolt_compute_serialize": True})

    def to_nbt(self, mc: Mecha) -> AstNbt:
        return nbt_string(self, self.reference.get_value())

@dataclass(frozen=True, slots=True)
class AstIntegerBoltVariable(AstBaseInteger):
    type = "bolt_compute_variable"
    value: AstIdentifier | AstFormatString = required_field(metadata={"bolt_compute_serialize": True})

    def to_nbt(self, mc: Mecha) -> AstNbt:
        # bolt evaluates the variable before the transform step
        value: Any = self.value
        if isinstance(value, int) and not isinstance(value, bool):
            node = AstIntegerConstant(value=value)
        elif isinstance(value, str):
            node = AstIntegerReference(reference=AstResourceLocation.from_value(value))
        else:
            raise set_location(Diagnostic("error", f"Expected an integer or a number provider id but got {value!r}."), self)
        return set_location(node, self).to_nbt(mc)
@dataclass(frozen=True, slots=True)
class AstIntegerBinomial(AstBaseInteger):
    type = "binomial"
    n: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})
    p: AstBaseFloat = required_field(metadata={"bolt_compute_serialize": True})


@dataclass(frozen=True, slots=True)
class AstIntegerConditional(AstBaseInteger):
    type = "conditional"
    condition: AstResourceLocation | AstNbtCompound | AstNbtList = required_field(metadata={"bolt_compute_serialize": True})
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
class AstIntegerPow(AstBaseInteger):
    type = "pow"
    base: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})
    exponent: AstBaseInteger = required_field(metadata={"bolt_compute_serialize": True})
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
class AstIntegerConstant(AstBaseInteger):
    type = "constant"
    value: int = required_field(metadata={"bolt_compute_serialize": True})

    def to_nbt(self, mc: Mecha) -> AstNbt:
        return set_location(AstNbtValue(value=Int(self.value)), self)


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

    def to_nbt(self, mc: Mecha) -> AstNbt:
        target = {"type": field_to_nbt(self.target_type, mc)}
        if self.target_target:
            target["target"] = field_to_nbt(self.target_target, mc)
        if self.target_name:
            target["name"] = field_to_nbt(self.target_name, mc)
        entries = {
            "type": nbt_string(self, "minecraft:score"),
            "target": nbt_compound(self, target),
            "score": field_to_nbt(self.score, mc),
        }
        if self.fallback:
            entries["fallback"] = self.fallback.to_nbt(mc)
        return nbt_compound(self, entries)


@dataclass(frozen=True, slots=True)
class AstIntegerScoreResolveLater(AstBaseInteger):
    type = "bolt_compute_score_resolve_later"
    args: AstChildren[AstNodeContainer] = required_field()

    def to_nbt(self, mc: Mecha) -> AstNbt:
        return self.resolve().to_nbt(mc)

    def resolve(self) -> AstIntegerScore:
        # bolt evaluates the arguments before the transform step
        arr = deque([x.value for x in self.args])
        first = arr.popleft()
        if first in AstTargetType.options:
            target_type = AstTargetTypeType.from_value("context")
            target_target = AstTargetType.from_value(first)
            target_name = None
            score = AstObjective.from_value(arr.popleft())
        elif first in AstTargetTypeType.options:
            target_type = AstTargetTypeType.from_value(first)
            if first == "fixed":
                target_target = None
                name = arr.popleft()
                try:
                    target_name = AstPlayerName.from_value(name)
                except ValueError:
                    target_name = AstUUID.from_value(name)
            elif first == "context":
                target_name = None
                name = arr.popleft()
                target_target = AstTargetType.from_value(name)
            score = AstObjective.from_value(arr.popleft())
        else:
            raise set_location(Diagnostic("error", f"{first!r} is not in {AstTargetType.options} or {AstTargetTypeType.options}."), self)

        fallback = None
        if len(arr) > 0:
            fallback = arr.popleft()

        if isinstance(fallback, str):
            fallback = AstIntegerReference(reference=AstResourceLocation.from_value(fallback))
        elif isinstance(fallback, int):
            fallback = AstIntegerConstant(value=fallback)
        elif fallback is None:
            ...
        else:
            raise set_location(Diagnostic("error", f"Expected an integer or a number provider id as fallback but got {fallback!r}."), self)

        if len(arr) > 0:
            raise set_location(Diagnostic("error", f"Too many arguments for the score literal, {list(arr)} are left."), self)

        node = AstIntegerScore(target_type=target_type, target_target=target_target, target_name=target_name, score=score, fallback=fallback)
        return set_location(node, self)





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
