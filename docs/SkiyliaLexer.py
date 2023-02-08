#
# File used for syntax-highlighting code sections in the documentation.
#

import os
import re

from pygments import unistring as uni
from pygments.lexer import RegexLexer, bygroups, default, include, words
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text,
    Whitespace,
)


class SkiyliaLexer(RegexLexer):
    name = "Skiylia"
    aliases = ["skiylia"]
    filenames = ["*.skiy"]

    # We lean very heavily on
    # https://github.com/KSP-KOS/KOS/blob/master/doc/KerboscriptLexer.py
    # for help here

    flags = re.MULTILINE

    __all__ = ["SkiyliaLexer"]

    uni_name = "[%s][%s]*" % (uni.xid_start, uni.xid_continue)

    tokens = {
        "root": [
            (r"\n", Whitespace),
            # comments
            (r"// [^\n]*[\n]", Comment.Single),
            (r"/// [^///]* ///", Comment.Multiline),
            # strings
            (r'"[^"]*"', String),
            (r"'[^']*'", String),
            (r"`[^`]*`", String),
            # operators
            (r"\.\.|~~|!~|!==|===|!=|==|<<|>>|\?\?|\?\:|[-~+/*%=<>&^|?.:]", Operator),
            (r"(in|is|do|and|or|xor|not)\b", Operator.Word),
            (r"[]{}:(),;[]", Punctuation),
            # text
            (r"[^\S\n]+", Text),
            (r"\\\n", Text),
            (r"\\", Text),
            # include other rules
            include("keywords"),
            include("numbers"),
            # functions
            (r"(def)((?:\s|\\\s)+)", bygroups(Keyword, Text), "funcname"),
            # classes
            (uni_name, Name.Class, "#pop"),
            # names and stuff
            (uni_name, Name),
        ],
        "keywords": [
            (
                words(
                    (
                        "break",
                        "continue",
                        "elif",
                        "else",
                        "for",
                        "if",
                        "while",
                        "when",
                        "until",
                        "then",
                        "return",
                    ),
                    suffix=r"\b",
                ),
                Keyword,
            ),
            (words(("true", "false", "null"), suffix=r"\b"), Keyword.Constant),
            (
                words(
                    (
                        "abs",
                        "arity",
                        "assert",
                        "bin",
                        "ceil",
                        "child",
                        "const",
                        "cplx",
                        "dict",
                        "doc",
                        "enter",
                        "errorfull",
                        "errorless",
                        "except",
                        "exception",
                        "float",
                        "floor",
                        "frac",
                        "from",
                        "hex",
                        "import",
                        "init",
                        "instance",
                        "int",
                        "iter",
                        "kill",
                        "leave",
                        "len",
                        "list",
                        "module",
                        "name",
                        "oct",
                        "params",
                        "parent",
                        "partial",
                        "private",
                        "property",
                        "raise",
                        "repr",
                        "round",
                        "select",
                        "set",
                        "sibling",
                        "stack",
                        "stnd",
                        "str",
                        "timed",
                        "trn",
                        "try",
                        "var",
                        "xor",
                    ),
                    prefix=r"(?<!\.)",
                    suffix=r"\b",
                ),
                Name.Builtin,
            ),
        ],
        "numbers": [
            (r"\d+\.\d+", Number.Float),
            (r"0[oO](?:[0-7])+", Number.Oct),
            (r"0[bB](?:[01])+", Number.Bin),
            (r"0[xX](?:[a-fA-F0-9])+", Number.Hex),
            (r"\d+", Number.Integer),
        ],
        "funcname": [
            (uni_name, Name.Function, "#pop"),
            default("#pop"),
        ],
    }


def setup(app):
    app.add_lexer("SkiyliaLexer", SkiyliaLexer())
