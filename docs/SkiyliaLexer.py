#
# File used for syntax-highlighting code sections in the documentation.
#

import re

from pygments.lexer import RegexLexer, words
from pygments.token import (
    Comment,
    Keyword,
    Name,
    Number,
    Operator,
    Punctuation,
    String,
    Text)


class SkiyliaLexer(RegexLexer):

    name = 'Skiylia'
    aliases = ['skiylia']
    filenames = ['*.skiy']

    # We lean very heavily on
    # https://github.com/KSP-KOS/KOS/blob/master/doc/KerboscriptLexer.py
    # for help here

    flags = re.MULTILINE

    __all__ = ['SkiyliaLexer']

    tokens = {
        'root': [
            (r"//  [^\r\n]*[\r\n]", Comment.Single),
            (r"/// [^\r\n]*(\n\t.+)+ ///", Comment.Multiline),

            (r'"[^"]*"', String),
            (r"'[^']*'", String),

            (r'[+\-*/><=~]', Operator),
            (r'[(),]', Punctuation),

            (words(("print"), suffix=r'\b'), Keyword),

            (r'\b[a-z_][a-z_\d]*\b', Name.Variable),

            (r'[\t\s\r\n]+', Text),
            (r'\b(\d+)+\b', Number),
        ]
    }


def setup(app):
    app.add_lexer("skiylia", SkiyliaLexer())
