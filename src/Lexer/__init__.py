# Skiylia Lexer, converts source code to recognised tokens

from typing import Any

from skiylia_errors import (
    UnidentifiedCharacter,
    UnterminatedComment,
    UnterminatedString,
)

from .grammar_rules import string_chars, symbols
from .tokens import Token


def Lex(program: str, debug: bool = False) -> list[Token]:
    lexer = Lexer(program, debug)
    return lexer.lexAll()


class Lexer:
    def __init__(self, program: str, debug: bool = False) -> None:
        self.pos: int = 0
        self.row: int = 1
        self.column: int = 1
        if program[-1] != "\0":
            program += "\0"
        self.source: str = program
        self.sourcelen: int = len(program)
        self.debug = debug
    
    def lexAll(self) -> list[Token]:
        """Continue to parse source code until we complete the token stream."""
        toks: list[Token] = []
        while not self.atEnd():
            toks.append(self.lex())
        return toks

    def lex(self) -> Token:
        """Parse the next token from the soure code"""
        lastrow = self.row if self.pos > 0 else 0
        token = self.scanToken()
        if self.debug:
            row = token.row
            tpe, lex = token.rep()
            print("   |" if row == lastrow else f"{row:4d}",
                tpe.rjust(10),
                lex)
            lastrow = row
        return token

    def scanToken(self) -> Token:
        """Fetch the next token in the source."""
        if self.peekGroup(2) == "//":
            return self.createCommentToken()

        c = self.advance()

        symb = symbols.get(c, "")
        if symb:
            return self.createToken(symb, c)
        if c.isdigit():
            return self.createNumberToken(c)
        elif c.isalpha():
            return self.createIdentifierToken(c)
        elif c in string_chars:
            return self.createStringToken(c)
        # return self.createToken("UNKNOWN_TOKEN", c)
        raise UnidentifiedCharacter(self.column, self.row, c)

    def createToken(self, tpe: str, lexeme: str, literal: Any = None) -> Token:
        if lexeme == " " and self.matchGroup("   "):
            tpe, lexeme = "TAB", "    "
        return Token(tpe, lexeme, literal, self.column, self.row)

    def createNumberToken(self, lexeme: str = "") -> Token:
        while self.peek().isdigit():
            lexeme += self.advance()
        if self.peek() == ".":
            lexeme += self.advance()
            while self.peek().isdigit():
                lexeme += self.advance()
            return self.createToken("NUMBER", lexeme, float(lexeme))
        return self.createToken("NUMBER", lexeme, int(lexeme))

    def createIdentifierToken(self, lexeme: str = "") -> Token:
        while self.peek().isalnum():
            lexeme += self.advance()
        return self.createToken("IDENTIFIER", lexeme)

    def createStringToken(self, closure: str) -> Token:
        lexeme = ""
        c, r = (self.column, self.row)
        while not self.match(closure):
            if self.atEnd():
                self.exception(UnterminatedString, closure, col=c, row=r)
            lexeme += self.advance()
        self.advance()
        return self.createToken("STRING", lexeme)

    def createCommentToken(self) -> Token:
        lexeme = ""
        c, r = (self.column, self.row)
        self.advance(2)
        closure = "///" if self.match("/") else "\n"
        while not self.matchGroup(closure):
            if self.atEnd():
                self.exception(UnterminatedComment, closure, col=c, row=r)
            lexeme += self.advance()
        return self.createToken("COMMENT", lexeme)

    def peek(self, offset: int = 0) -> str:
        if self.pos + offset >= self.sourcelen:
            return "\0"
        return self.source[self.pos + offset]

    def peekGroup(self, offset: int = 1) -> str:
        if self.pos + offset >= self.sourcelen:
            return "\0"
        return self.source[self.pos : self.pos + offset]

    def match(self, char: str) -> bool:
        if self.peek() != char:
            return False
        self.advance()
        return True

    def matchGroup(self, chars: str) -> bool:
        clen = len(chars)
        if self.peekGroup(clen) != chars:
            return False
        self.advance(clen)
        return True

    def advance(self, offset: int = 1) -> str:
        self.pos += offset
        self.column += offset
        char = self.source[self.pos - offset]
        if char == "\n":
            self.row = 1
            self.column += 1
        return char

    def atEnd(self) -> bool:
        return self.pos >= self.sourcelen

    def exception(
        self,
        exception,
        message: str = "",
        location: str = "",
        col: int = 0,
        row: int = 0,
    ) -> None:
        if col and row:
            raise exception(col, row, message, location)
        raise exception(self.column, self.row, message, location)
