# Errors and exceptions specific to skiylia

from typing import Type


class SkiyliaError(Exception):
    """Base Skiylia error."""

    def __init__(
        self,
        col: int = 0,
        row: int = 0,
        message: str = "",
        location: str = "",
        *args,
    ) -> None:
        super().__init__(*args)
        self.col = col
        self.row = row
        self.message = message
        self.location = location
        self.err = "".join(
            " " + x if x.isupper() and i > 0 else x
            for i, x in enumerate(self.__class__.__name__)
        )

    def __str__(self) -> str:
        return (
            f"[Line {self.row}, Char {self.col}] {self.err}: {self.message}"
            if self.row or self.col
            else f"{self.err} at {self.location}: {self.message}"
        )


class UnidentifiedCharacter(SkiyliaError):
    """Raised when an unknown character is found in the filestream."""

    def __init__(self, col: int = 0, row: int = 0, char: str = "", *args) -> None:
        super().__init__(col, row, f"'{char}'")


class UnexpectedCharacter(SkiyliaError):
    """Raised when an unexpected character occurs in the filestream."""


class UnterminatedClosure(SkiyliaError):
    """Used when an opening literal is not closed."""

    def __init__(self, col: int = 0, row: int = 0, char: str = "", *args) -> None:
        antichar = {
            "(": ")",
            "[": "]",
            "{": "}",
            "\n": "\\n",
        }.get(char, char)
        quote = "'" if antichar != "'" else "`"
        super().__init__(col, row, f"Missing {quote}{antichar}{quote}")


class UnterminatedString(UnterminatedClosure):
    """Raised when a string is not terminated correctly."""


class UnterminatedComment(UnterminatedClosure):
    """Raised when a comment is not terminated correctly."""


class error:
    UNIDENTIFIEDCHARACTER = 1
    UNEXPECTEDCHARACTER = 2

    UNTERMINATEDCLOSURE = 3
    UNTERMINATEDSTRING = 4
    UNTERMINATEDCOMMENT = 5

    def reverse(self, code: int = 0) -> Type[SkiyliaError]:
        match code:
            case self.UNIDENTIFIEDCHARACTER:
                return UnidentifiedCharacter
            case self.UNEXPECTEDCHARACTER:
                return UnexpectedCharacter
            case self.UNTERMINATEDCLOSURE:
                return UnterminatedClosure
            case self.UNTERMINATEDSTRING:
                return UnterminatedString
            case self.UNTERMINATEDCOMMENT:
                return UnterminatedComment
            case _:
                return SkiyliaError
