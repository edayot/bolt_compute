from beet import Context
from mecha import (
    BasicLiteralParser,
    CommandTree,
    Mecha,
    MultilineParser,
    delegate,
)

from bolt_compute.integer import AstTargetType, AstTargetTypeType
from bolt_compute.node import serialize_node
from bolt_compute.parser import operation_parser


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


def beet_default(ctx: Context):
    mc = ctx.inject(Mecha)
    mc.spec.parsers["command:argument:minecraft:context_float_provider"] = (
        MultilineParser(delegate("resource_location_or_nbt"))
    )
    mc.spec.parsers["command:argument:minecraft:context_int_provider"] = (
        MultilineParser(delegate("resource_location_or_nbt"))
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
