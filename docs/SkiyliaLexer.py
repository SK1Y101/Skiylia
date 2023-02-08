#
# File used for syntax-highlighting code sections in the documentation.
#

import re

from pygments.lexer import RegexLexer, include, bygroups, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Whitespace
from pygments import unistring as uni

class SkiyliaLexer(RegexLexer):

    name = 'Skiylia'
    aliases = ['skiylia']
    filenames = ['*.skiy']

    # We lean very heavily on
    # https://github.com/KSP-KOS/KOS/blob/master/doc/KerboscriptLexer.py
    # for help here

    flags = re.MULTILINE

    __all__ = ['SkiyliaLexer']

    uni_name = "[%s][%s]*" % (uni.xid_start, uni.xid_continue)

    tokens = {
        "root": [
            (r"\n", Whitespace),

            (r"//  [^\n]*[\n]", Comment.Single),
            (r"/// [^///]* ///", Comment.Multiline),

            (r'"[^"]*"', String),
            (r"'[^']*'", String),
            (r"`[^`]*`", String),

            (r'!=|==|<<|>>|:=|[-~+/*%=<>&^|.]', Operator),
            (r'[]{}:(),;[]', Punctuation),
            (r'(in|is|and|or|not)\b', Operator.Word),

            (r'[^\S\n]+', Text),

            include("keywords"),
            include("numbers"),

            (r'(def)((?:\s|\\\s)+)', bygroups(Keyword, Text), 'funcname'),
        ],
        "keywords": [
            (words(("break", "continue", "elif", "else", "for", "if", "return"), suffix=r'\b'), Keyword),
            (words(('true', 'false', 'null'), suffix=r'\b'), Keyword.Constant),
        ],
        "numbers": [
            (r'\d+\.\d+', Number.Float),
            (r'0[oO](?:[0-7])+', Number.Oct),
            (r'0[bB](?:[01])+', Number.Bin),
            (r'0[xX](?:[a-fA-F0-9])+', Number.Hex),
            (r'\d+', Number.Integer),
        ],
        "funcname": [
            (uni_name, Name.Function, '#pop'),
            default('#pop'),
        ],
    }


def setup(app):
    app.add_lexer("SkiyliaLexer", SkiyliaLexer())
