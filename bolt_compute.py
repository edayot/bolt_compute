from beet import Context
from beet.core.utils import JsonDict
from mecha import Mecha, delegate, MultilineParser, CommandTree
from bolt.pattern import STRING_PATTERN
from tokenstream import TokenStream, Token


def iter_compute_tree(tree: CommandTree):
    if tree.children:
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
                                        

def parse_literal(stream: TokenStream) -> JsonDict | float | str:
    token = stream.expect_any("oparent", "numeric", "quotes")
    match token:
        case Token("oparent"):
            raise NotImplementedError()
        case Token("numeric"):
            
            return float(token.value)
        case Token("quotes"):
            parser = delegate("bolt:expression")
            res = stream.expect("resource")
            stream.expect("quotes")
            return res.value
    raise NotImplementedError("UNREACHABLE")


def operation_parser(stream: TokenStream):
    """Parse operation."""
    res = {}
    with stream.syntax(
        oparent=r"\(",
        cparent=r"\)",
        operation=r"\+|\-|\*|\/",
        number=r"[+-]?([0-9]*[.])?[0-9]+",
        quotes=r'"',
        resource=STRING_PATTERN,
    ):
        stream.expect("oparent")
        parse_literal(stream)
        stream.expect("cparent")
        



def beet_default(ctx: Context):
    mc = ctx.inject(Mecha)
    mc.spec.parsers["command:argument:minecraft:number_provider"] = MultilineParser(delegate("resource_location_or_nbt"))

    for compute in iter_compute_tree(mc.spec.tree):
        if compute.children:
            compute.children["bolt"] = CommandTree(**{
                "type": "literal",
                "children": {
                    "operation": {
                        "type": "argument",
                        "parser": "bolt_compute:operation_parser"
                    }
                }
            })

    mc.spec.parsers["command:argument:bolt_compute:operation_parser"] = MultilineParser(operation_parser)

        
    mc.spec.update()
