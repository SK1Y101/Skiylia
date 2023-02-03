# Tests to verify the correct functioning of the Skiylia lexer

from .fixtures import decompose, lexer  # isort:skip

from skiylia_errors import error


class TestLexerLexes:
    """Test the lexer generates the correct token streams."""

    def test_debug(self, lexer: lexer, capsys) -> None:
        num1, op, num2, string = 1, "+", 2, "hello world!"
        lexer(f"{num1}{op}{num2}\n'{string}'", True)
        assert capsys.readouterr().out.split("\n") == [
            f"{1:4d} {'NUMBER'.rjust(10)} '{num1}': {float(num1)}",
            f"   | {'PLUS'.rjust(10)} '+'",
            f"   | {'NUMBER'.rjust(10)} '{num2}': {float(num2)}",
            f"   | {'NEWLINE'.rjust(10)} '\\n'",
            f"{2:4d} {'STRING'.rjust(10)} '{string}'",
            f"   | {'EOF'.rjust(10)} '\\0'",
            "",
        ]

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
        assert tokens.lexemes == [comment1, "\\n", comment2, "\\0"]

    def test_comment_multi(self, lexer: lexer) -> None:
        comment = "This is a multi-\n\tline comment\n"
        token = lexer(f"///{comment}///")[0]
        assert token.type == "COMMENT"
        assert token.lexeme == comment

    def test_comment_fails(self, lexer: lexer) -> None:
        tokens = lexer("// failed single comment")
        err_token = [token for token in tokens if token.type == "ERROR"][0]
        assert (err_token.type, err_token.lexeme, err_token.literal) == (
            "ERROR",
            "\\n",
            error.UNTERMINATEDCOMMENT,
        )

        tokens = lexer("/// failed multi-line comment")
        err_token = [token for token in tokens if token.type == "ERROR"][0]
        assert (err_token.type, err_token.lexeme, err_token.literal) == (
            "ERROR",
            "///",
            error.UNTERMINATEDCOMMENT,
        )

    def test_string(self, decompose: decompose) -> None:
        string1 = "hello"
        string2 = "world"
        tokens = decompose(f"'{string1}'\n \"{string2}\"")
        assert tokens.lexemes == [string1, "\\n", " ", string2, "\\0"]
        assert tokens.types == ["STRING", "NEWLINE", "SPACE", "STRING", "EOF"]

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
        tokens = lexer("7.6.9")
        err_token = [token for token in tokens if token.type == "ERROR"][0]
        assert (err_token.type, err_token.lexeme, err_token.literal) == (
            "ERROR",
            ".",
            error.UNIDENTIFIEDCHARACTER,
        )
        tokens = lexer(".90")

        err_token = [token for token in tokens if token.type == "ERROR"][0]
        assert (err_token.type, err_token.lexeme, err_token.literal) == (
            "ERROR",
            ".",
            error.UNIDENTIFIEDCHARACTER,
        )

    def test_identifier(self, lexer: lexer) -> None:
        ident = "testvar"
        token = lexer(ident)[0]
        assert token.type == "IDENTIFIER"
        assert token.lexeme == ident
