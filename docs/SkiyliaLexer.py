#
# File used for syntax-highlighting code sections in the documentation.
#

import re

from pygments.lexer import RegexLexer, include, bygroups, using, \
    this, inherit, default, words
from pygments.util import get_bool_opt
from pygments.token import Text, Comment, Operator, Keyword, Name, String, \
    Number, Punctuation, Error

class SkiyliaLexer(RegexLexer):
   
    name = 'Skiylia'
    aliases = ['skiylia']
    filenames = ['*.skiy']

    # We lean very heavily on https://github.com/KSP-KOS/KOS/blob/master/doc/KerboscriptLexer.py for help here
 
    flags = re.MULTILINE

    __all__ = ['SkiyliaLexer']

    tokens = {
        'root': [
            (r"//  [^\r\n]*[\r\n]", Comment.Single),
            (r"/// [^\r\n]*(\n\t.+)+ ///", Comment.Multiline),
        ]
    }

def setup(app):
    app.add_lexer("skiylia", SkiyliaLexer())
