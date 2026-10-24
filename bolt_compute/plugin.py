from copy import deepcopy
from dataclasses import dataclass
from typing import Iterable

from beet import Context, configurable
from bolt import Accumulator, AstExpression, Runtime, AstAssignment, AstTargetIdentifier, AstValue, LexicalScope, get_stream_lexical_scope
from bolt.pattern import IDENTIFIER_PATTERN
from mecha import (
    AlternativeParser,
    AstBool,
    AstChildren,
    AstCommand,
    AstCommandSentinel,
    AstNbtPath,
    AstNbtPathKey,
    AstNode,
    AstResourceLocation,
    BasicLiteralParser,
    CommandTree,
    Mecha,
    MultilineParser,
)
from pydantic import BaseModel

from bolt_compute.integer import AstTargetType, AstTargetTypeType
from bolt_compute.node import serialize_node
from bolt_compute.parser import as_mecha_parser, operation_parser
from bolt_compute.using_command import USING_COMMAND_TREE, UsingCommandParser, UsingCommandTransformer, codegen_using_command, serialize_using


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
    using_keyword: bool = False




@configurable("bolt_compute", validator=BoltComputeOpts)
def beet_default(ctx: Context, opts: BoltComputeOpts):
    mc = ctx.inject(Mecha)
    if opts.default_command:
        mc.spec.parsers["command:argument:minecraft:context_float_provider"] = (
            AlternativeParser([MultilineParser(as_mecha_parser("float", 0)), mc.spec.parsers["command:argument:minecraft:context_float_provider"], ])
        )
        mc.spec.parsers["command:argument:minecraft:context_int_provider"] = (
            AlternativeParser([MultilineParser(as_mecha_parser("integer", 0)), mc.spec.parsers["command:argument:minecraft:context_int_provider"], ])
        )
    if opts.using_keyword:
        runtime = ctx.inject(Runtime)
        runtime.modules.codegen.add_rule(codegen_using_command)
        mc.serialize.add_rule(serialize_using)
        mc.spec.add_commands(USING_COMMAND_TREE)
        mc.spec.parsers["command:argument:bolt_compute:using_command"] = UsingCommandParser()
        mc.transform.extend(UsingCommandTransformer())

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
