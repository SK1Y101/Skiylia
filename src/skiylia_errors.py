# Errors and exceptions specific to skiylia


class SkiyliaError(Exception):
    """Base Skiylia error."""

    errcode = 0

    def __init__(
        self,
        column: int = 0,
        row: int = 0,
        message: str = "",
        location: str = "",
        *args,
    ) -> None:
        super().__init__(*args)
        self.column = column
        self.row = row
        self.message = message
        self.location = location
        self.err = self.__class__.__name__

    def __str__(self) -> str:
        return (
            f"[Line {self.column}, Col {self.row}] {self.err}: {self.message}"
            if self.row or self.column
            else f"{self.err} at {self.location}: {self.message}"
        )


class UnidentifiedCharacter(SkiyliaError):
    """Raised when an unknown character is found in the filestream."""

    def __init__(self, column: int = 0, row: int = 0, char: str = "") -> None:
        super().__init__(column, row, f"'{char}'")


class UnexpectedCharacter(SkiyliaError):
    """Raised when an unexpected character occurs in the filestream."""

    errcode = 1
