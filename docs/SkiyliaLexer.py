#
# File used for syntax-highlighting code sections in the documentation.
#

import os
import re

from pygments import unistring as uni
from pygments.lexer import RegexLexer, bygroups, combined, default, include, words
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

    def fstring_rules(ttype):
        return [
            # Assuming that a '}' is the closing brace after format specifier.
            # Sadly, this means that we won't detect syntax error. But it's
            # more important to parse correct syntax correctly, than to
            # highlight invalid syntax.
            (r'\}', String.Interpol),
            (r'\{', String.Interpol, 'expr-inside-fstring'),
            # backslashes, quotes and formatting signs must be parsed one at a time
            (r'[^\\\'"{}\n]+', ttype),
            (r'[\'"\\]', ttype),
            # newlines are an error (use "nl" state)
        ]

    tokens = {
        "root": [
            (r"\n", Whitespace),
            # comments
            (r"// [^\n]*[\n]", Comment.Single),
            (r"/// [^///]* ///", Comment.Multiline),
            # functions
            (r"(def)((?:\s|\\\s)+)", bygroups(Keyword, Text), "funcname"),
            # classes
            (uni_name, Name.Class, "#pop"),
            # expressions
            include("expression"),
        ],
        "expression": [
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
            # names and stuff
            (uni_name, Name),
            # interpolated strings
            ('([fF])(")', bygroups(String.Affix, String.Double),
             combined('fstringescape', 'dqf')),
            ("([fF])(')", bygroups(String.Affix, String.Single),
             combined('fstringescape', 'sqf')),
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
        'expr-inside-fstring': [
            (r'[{([]', Punctuation, 'expr-inside-fstring-inner'),
            # without format specifier
            (r'(=\s*)?'         # debug (https://bugs.python.org/issue36817)
             r'(\![sraf])?'     # conversion
             r'\}', String.Interpol, '#pop'),
            # with format specifier
            # we'll catch the remaining '}' in the outer scope
            (r'(=\s*)?'         # debug (https://bugs.python.org/issue36817)
             r'(\![sraf])?'     # conversion
             r':', String.Interpol, '#pop'),
            (r'\s+', Whitespace),  # allow new lines
            include('expr'),
        ],
        'expr-inside-fstring-inner': [
            (r'[{([]', Punctuation, 'expr-inside-fstring-inner'),
            (r'[])}]', Punctuation, '#pop'),
            (r'\s+', Whitespace),  # allow new lines
            include('expr'),
        ],
        'fstringescape': [
            include('rfstringescape'),
            include('stringescape'),
        ],
        'fstrings-single': fstring_rules(String.Single),
        'fstrings-double': fstring_rules(String.Double),
        'dqf': [
            (r'"', String.Double, '#pop'),
            include('fstrings-double')
        ],
        'sqf': [
            (r"'", String.Single, '#pop'),
            include('fstrings-single')
        ],
    }


def setup(app):
    app.add_lexer("SkiyliaLexer", SkiyliaLexer())
