# Tests to verify the correct functioning of the Skiylia lexer

import sys
sys.path.append("src")

from lexer import Lex
from lexer.tokens import Token

class TestLexerLexes:

    def test_comment_single(self) -> None:
        comment = "Example comment"
        token = Lex(f"//{comment}")
        assert token[0].lexeme == comment
    
    def test_comment_multi(self) -> None:
        comment = "This is a multi-\n\tline comment"
        token = Lex(f"///{comment}///")
        assert token[0].lexeme == comment
