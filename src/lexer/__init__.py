# Skiylia Lexer, converts source code to recognised tokens

from typing import Any

from skiylia_errors import UnidentifiedCharacter

from .grammar_rules import symbols
from .tokens import Token


def Lex(program: str) -> list[Token]:
    lexer = Lexer(program)
    return lexer.lex()


class Lexer:
    def __init__(self, program: str) -> None:
        self.pos: int = 0
        self.row: int = 1
        self.column: int = 1
        if program[-1] != "\0":
            program += "\0"
        self.source: str = program
        self.sourcelen: int = len(program)

    def lex(self) -> list[Token]:
        """Continue to parse source code until we complete the token stream."""
        self.tokens = []
        while not self.atEnd():
            token = self.scanToken()
            self.tokens.append(token)
        return self.tokens

    def scanToken(self) -> Token:
        """Fetch the next token in the source."""
        c = self.advance()

        symb = symbols.get(c, "")
        if symb:
            return self.createToken(symb, c)

        if c.isdigit():
            return self.createNumberToken(c)

        elif c.isalpha():
            return self.createIdentifierToken(c)
        raise UnidentifiedCharacter(self.column, self.row, c)

    def createToken(self, tpe: str, lexeme: str, literal: Any = None) -> Token:
        if tpe == "NEWLINE":
            self.row = 1
            self.column += 1
        return Token(tpe, lexeme, literal, self.column, self.row)

    def createNumberToken(self, lexeme: str = "") -> Token:
        while self.peek().isdigit():
            lexeme += self.advance()

        # if self.peek() == ".":
        #     lexeme += self.advance()
        #     while self.peek().isdigit():
        #         lexeme += self.advance()
        #     return self.createToken("NUMBER", lexeme, float(lexeme))
        return self.createToken("NUMBER", lexeme, int(lexeme))

    def peek(self, offset: int = 0) -> str:
        if self.pos + offset <= self.sourcelen:
            return self.source[self.pos + offset]
        return "\0"

    def advance(self) -> str:
        self.pos += 1
        self.row += 1
        if self.atEnd():
            return "\0"
        return self.source[self.pos - 1]

    def atEnd(self) -> bool:
        return self.pos >= self.sourcelen
