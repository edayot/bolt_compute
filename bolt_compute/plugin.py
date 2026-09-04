from beet import Context
from mecha import (
    CommandTree,
    Mecha,
    MultilineParser,
    delegate,
)

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
    # rules = [
    #     serialize_operation,
    #     serialize_resource_location,
    #     serialize_root,
    #     serialize_storage,
    #     serialize_bolt_value,
    #     serialize_compute_number,
    #     serialize_list_call,
    #     serialize_compute_binomial,
    #     serialize_compute_uniform,
    #     serialize_compute_conditional,
    #     serialize_compute_score,
    # ]
    # for r in rules:
    #     mc.serialize.add_rule(r)

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

    mc.spec.update()
