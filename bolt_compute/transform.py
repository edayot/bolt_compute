from dataclasses import dataclass, replace

from beet.core.utils import required_field
from mecha import AstChildren, AstCommand, Diagnostic, Mecha, MutatingReducer, rule
from tokenstream import set_location

from bolt_compute.node import AstBaseNode, AstComputeRoot
from bolt_compute.types import BoltType

COMPUTE_BOLT_SUFFIX = "compute:bolt"

COMPUTE_TARGETS: dict[BoltType, str] = {
    "default": "compute:default",
    "entity": "compute:entity:computeTarget",
    "block": "compute:block:computePos",
}


@dataclass
class BoltComputeTransformer(MutatingReducer):
    """Transformer that turns bolt_compute expressions into vanilla number providers."""

    mc: Mecha = required_field()

    @rule(AstCommand)
    def compute_command(self, node: AstCommand):
        if not any(isinstance(argument, (AstBaseNode, AstComputeRoot)) for argument in node.arguments):
            return node

        identifier = node.identifier
        arguments = []

        for argument in node.arguments:
            if isinstance(argument, AstComputeRoot):
                # rewrite `compute bolt...` into the matching vanilla `compute` command
                prefix = identifier.removesuffix(COMPUTE_BOLT_SUFFIX)
                identifier = f"{prefix}{COMPUTE_TARGETS[argument.bolt_type]}:{argument.operation_type}:provider"
                if argument.argument_node is not None:
                    arguments.append(argument.argument_node)
                arguments.append(argument.children.to_provider(self.mc))
            elif isinstance(argument, AstBaseNode):
                arguments.append(argument.to_provider(self.mc))
            else:
                arguments.append(argument)

        if identifier not in self.mc.spec.prototypes:
            raise set_location(Diagnostic("error", f"Unknown command {identifier!r}."), node)

        return replace(node, identifier=identifier, arguments=AstChildren(arguments))
