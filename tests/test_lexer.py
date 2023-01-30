# Tests to verify the correct functioning of the Skiylia lexer

import pytest

from .fixtures import decompose, lexer
from skiylia_errors import UnidentifiedCharacter, UnterminatedComment


class TestLexerLexes:
    """Test the lexer generates the correct token streams."""

    def test_comment_single(self, lexer: lexer) -> None:
        comment = "Example comment"
        token = lexer(f"//{comment}\n")[0]
        assert token.type == "COMMENT"
        assert token.lexeme == comment

    def test_comment_multiple_single(self, decompose: decompose) -> None:
        comment1 = "Example comment"
        comment2 = "second comment"
        tokens = decompose(f"//{comment1}\n\n//{comment2}\n")
        assert tokens.types == ["COMMENT", "NEWLINE", "COMMENT", "EOF"]
        assert tokens.lexemes == [comment1, "\n", comment2, "\0"]

    def test_comment_multi(self, lexer: lexer) -> None:
        comment = "This is a multi-\n\tline comment\n"
        token = lexer(f"///{comment}///")[0]
        assert token.type == "COMMENT"
        assert token.lexeme == comment

    def test_comment_fails(self, lexer: lexer) -> None:
        with pytest.raises(UnterminatedComment):
            lexer("// failed single comment")

        with pytest.raises(UnterminatedComment):
            lexer("/// failed multi-line comment")

    def test_number_integer(self, lexer: lexer) -> None:
        number = "1"
        token = lexer(number)[0]
        assert token.type == "NUMBER"
        assert token.lexeme == number
        assert token.literal == int(number)

    def test_number_float(self, lexer: lexer) -> None:
        number = "45.9"
        token = lexer(number)[0]
        assert token.type == "NUMBER"
        assert token.lexeme == number
        assert token.literal == float(number)

    def test_number_fails(self, lexer: lexer) -> None:
        with pytest.raises(UnidentifiedCharacter):
            lexer("7.6.9")

        with pytest.raises(UnidentifiedCharacter):
            lexer(".90")

    def test_identifier(self, lexer: lexer) -> None:
        ident = "testvar"
        token = lexer(ident)[0]
        assert token.type == "IDENTIFIER"
        assert token.lexeme == ident
