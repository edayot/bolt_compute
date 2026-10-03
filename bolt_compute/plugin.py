from beet import Context, configurable
from mecha import (
    AlternativeParser,
    BasicLiteralParser,
    CommandTree,
    Mecha,
    MultilineParser,
    delegate,
)
from pydantic import BaseModel

from bolt_compute.integer import AstTargetType, AstTargetTypeType
from bolt_compute.node import serialize_node
from bolt_compute.parser import as_mecha_parser, operation_parser


def iter_compute_tree(tree: CommandTree):
    if tree.children:
        compute = tree.children["compute"]
        if compute.children:
            yield compute

        data = tree.children["data"]
        if data.children:
            modify = data.children["modify"]
            if modify.children:
                childs = [
                    "block",
                    "entity",
                    "storage",
                ]
                for c in childs:
                    child = modify.children[c]
                    if child.children:
                        target = child.children["target"]
                        if target.children:
                            targetPath = target.children["targetPath"]
                            if targetPath.children:
                                for o in [
                                    "append",
                                    "merge",
                                    "prepend",
                                    "set",
                                ]:
                                    operation = targetPath.children[o]
                                    if operation.children:
                                        compute = operation.children["compute"]
                                        yield compute
                                insert = targetPath.children["insert"]
                                if insert.children:
                                    index = insert.children["index"]
                                    if index.children:
                                        compute = index.children["compute"]
                                        yield compute

class BoltComputeOpts(BaseModel):
    default_command: bool = True
    """
        Makes bolt_compute expressions available to all commands 
        using `command:argument:minecraft:context_float_provider` or `command:argument:minecraft:context_int_provider`

        `bolt`, `bolt_block`, `bolt_entity` keywords are used if this value is False
    """


@configurable("bolt_compute", validator=BoltComputeOpts)
def beet_default(ctx: Context, opts: BoltComputeOpts):
    mc = ctx.inject(Mecha)
    if opts.default_command:
        mc.spec.parsers["command:argument:minecraft:context_float_provider"] = (
            AlternativeParser([mc.spec.parsers["command:argument:minecraft:context_float_provider"], MultilineParser(as_mecha_parser("float", 0))])
        )
        mc.spec.parsers["command:argument:minecraft:context_int_provider"] = (
            AlternativeParser([mc.spec.parsers["command:argument:minecraft:context_int_provider"], MultilineParser(as_mecha_parser("integer", 0))])
        )
    mc.serialize.add_rule(serialize_node)

    for compute in iter_compute_tree(mc.spec.tree):
        if compute.children:
            compute.children["bolt"] = CommandTree(
                type= "argument",
                executable= True,
                parser = "bolt_compute:operation_parser",
            )

    mc.spec.parsers["command:argument:bolt_compute:operation_parser"] = MultilineParser(
        operation_parser
    )
    mc.spec.parsers.update({
        "bolt_compute_ast_target_type": BasicLiteralParser(AstTargetType),
        "bolt_compute_ast_target_type_type": BasicLiteralParser(AstTargetTypeType),
    })

    mc.spec.update()
