# Skiylia Token class, used to symbolically represent chunks of source code

from typing import Any


class Token:
    def __init__(
        self, type: str, lexeme: str, literal: Any = None, col: int = 0, row: int = 0
    ) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.col = col
        self.row = row

    def __repr__(self) -> str:
        if self.literal:
            return f"{self.type} '{self.lexeme}': {float(self.literal)}"
        return f"{self.type} '{self.lexeme}'"
