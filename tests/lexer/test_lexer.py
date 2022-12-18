# Pytests to test the Skiylia Lexer.

from lexer import Lexer


class TestLexer:
    def test_lexer_creates_token(self) -> None:
        lexer = Lexer("hello world")
        tokens = lexer.lex()
        assert tokens
        print(tokens)
