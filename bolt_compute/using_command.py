
from copy import deepcopy
from dataclasses import dataclass
from typing import Iterable

from bolt import Accumulator, AstAssignment, AstTargetIdentifier, AstValue, LexicalScope, get_stream_lexical_scope
from bolt.pattern import IDENTIFIER_PATTERN
from mecha import (
    AstChildren,
    AstCommand,
    AstNbtPath,
    AstNbtPathKey,
    AstNode,
    AstResourceLocation,
    Visitor,
    delegate,
    rule,
)
from tokenstream import TokenStream, set_location

from beet.core.utils import required_field



USING_COMMAND_TREE = {
    "type": "root",
    "children": {
        "using": {
            "type": "literal",
            "executable": True,
            "children": {
                "children": {
                    "type": "argument",
                    "executable": True,
                    "parser": "bolt_compute:using_command"
                }
            }
        }
    },
}

class StorageRef:
    storage: AstResourceLocation
    nbt_path: AstNbtPath
    identifier: str

    def __init__(self, storage: AstResourceLocation, nbt_path: AstNbtPath, identifier: str) -> None:
        self.storage = storage
        self.nbt_path = nbt_path
        self.identifier = identifier
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(storage={self.storage}, nbt_path={self.nbt_path}, identifier={self.identifier})"

    def __getitem__(self, key):
        if not isinstance(self.nbt_path, AstNbtPath):
            raise KeyError(self)
        res = deepcopy(self)
        res.nbt_path = AstNbtPath(components=AstChildren(
            res.nbt_path.components + (AstNbtPathKey(value=str(key)),)
        ))
        return res

@dataclass(frozen=True, slots=True)
class AstUsingCommand(AstNode):
    using_command: StorageRef = required_field()
    assignment: AstAssignment = required_field()

@dataclass
class UsingCommandParser:
    """Parser for using command."""
    def __call__(self, stream: TokenStream):
        lexical_scope: LexicalScope = get_stream_lexical_scope(stream)

        with stream.syntax(storage="storage"):
            stream.expect("storage")

        resource_location = delegate("resource_location")(stream)

        nbt_path = None
        with stream.checkpoint() as commit:
            nbt_path = delegate("nbt_path")(stream)
            commit()


        with stream.syntax(**{
            "as": "as"
        }):
            begin = stream.expect("as")

        with stream.syntax(identifier=IDENTIFIER_PATTERN):
            identifier = stream.expect("identifier")
            
        using_command = StorageRef(storage=resource_location, nbt_path=nbt_path, identifier=identifier.value, )

        assignment = AstAssignment(operator="=", target=AstTargetIdentifier(value=identifier.value), value=AstValue(value=using_command))

        res = AstUsingCommand(assignment=assignment, using_command=using_command)

        lexical_scope.bind_variable(identifier.value, res)

        return set_location(res, begin, identifier)

@rule(AstUsingCommand)
def serialize_using(node: AstUsingCommand, result: list[str]) -> Iterable[AstNode] | None: 
    result.pop()
    result.pop()


class UsingCommandTransformer(Visitor):
    @rule(AstCommand, identifier="using:children")
    def using_command(self, node: AstCommand) -> AstCommand:
        return node


@rule(AstCommand, identifier="using:children")
def codegen_using_command(node: AstCommand, acc: Accumulator):
    using = node.arguments[0]
    assert isinstance(using, AstUsingCommand)
    value = acc.make_ref(using.using_command)
    acc.statement(f"{using.using_command.identifier} = {value}", lineno=using)
    return []

