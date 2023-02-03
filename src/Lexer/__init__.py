# Skiylia Lexer, converts source code to recognised tokens

from typing import Any

from skiylia_errors import error

from .lexical_rules import string_chars, symbols
from .tokens import Token


def Lex(program: str, debug: bool = False) -> list[Token]:
    lexer = Lexer(program, debug)
    return lexer.lexAll()


class Lexer:
    def __init__(self, program: str, debug: bool = False) -> None:
        self.current: int = 0
        self.currentrow: int = 1
        self.currentcol: int = 1

        self.debug = debug
        self.lastline: int = -1
        self.skipWhitespace = False

        self.source: str = program + "\0"

    def lexAll(self) -> list[Token]:
        """Continue to parse source code until we complete the token stream."""
        toks: list[Token] = []
        while not self.atEnd():
            tok = self.lex()
            toks.append(tok)
            if tok.type == "EOF":
                break
        return toks

    def lex(self, ignore_comment: bool = False) -> Token:
        """Parse the next token from the soure code"""
        token = self.scanToken()
        if ignore_comment:
            while token.type == "COMMENT":
                token = self.scanToken()
        if self.debug:
            line = token.row
            tpe, lex = token.rep()
            print(
                f"{line:4d}" if line != self.lastline else "   |",
                tpe.rjust(10),
                lex,
            )
            self.lastline = line
        return token

    """ Token Creation. """

    def scanToken(self) -> Token:
        """Fetch the next token in the source."""
        self.start = self.current
        self.startrow = self.currentrow
        self.startcol = self.currentcol

        if self.matchGroup("//"):
            return self.createCommentToken()
        elif self.skipWhitespace:
            while not self.atEnd() and self.peek() in [" ", "\t"]:
                self.advance()
                self.start += 1
                self.startcol += 1

        c = self.advance()

        match c:
            case c if c in symbols:
                return self.createToken(symbols[c])
            case c if c in string_chars:
                return self.createStringToken(c)
            case c if self.isalpha(c):
                return self.createIdentifierToken()
            case c if c.isdigit():
                return self.createNumberToken()
        return self.createErrorToken(error.UNIDENTIFIEDCHARACTER, c)

    def createToken(self, tpe: str, literal: Any = None) -> Token:
        if tpe == "SPACE" and self.matchGroup("   "):
            tpe = "TAB"
        self.skipWhitespace = tpe not in ["NEWLINE", "SPACE", "TAB"]
        return Token(tpe, self.lexeme, literal, self.startcol, self.startrow)

    def createErrorToken(self, errcode: int, message: str = "") -> Token:
        return Token("ERROR", message, errcode, self.startcol, self.startrow)

    def createClosureToken(
        self, tokenType: str, closure: str, error: int = error.UNTERMINATEDCLOSURE
    ) -> Token:
        while not self.matchGroup(closure):
            if self.atEnd():
                return self.createErrorToken(error, closure)
            self.advance()
        # Manipulate the start/end points to remove the closures
        self.start += len(closure)
        self.current -= len(closure)
        token = self.createToken(tokenType)
        self.current += len(closure)
        return token

    def createCommentToken(self) -> Token:
        closure = "///" if self.match("/") else "\n"
        # the starture length is one more than the closure length
        self.start += int(closure == "\n")
        return self.createClosureToken("COMMENT", closure, error.UNTERMINATEDCOMMENT)

    def createStringToken(self, closure: str) -> Token:
        return self.createClosureToken("STRING", closure, error.UNTERMINATEDSTRING)

    def createNumberToken(self) -> Token:
        while self.peek().isdigit():
            self.advance()
        if self.match(".") and self.peek().isdigit():
            while self.peek().isdigit():
                self.advance()
        return self.createToken("NUMBER", float(self.lexeme))

    def createIdentifierToken(self) -> Token:
        while self.isalphanum(self.peek()):
            self.advance()
        return self.createToken("IDENTIFIER")

    """ Helper functions. """

    def isalphanum(self, char: str) -> bool:
        return char.isalpha() or char.isdigit() or char == "_"

    def isalpha(self, char: str) -> bool:
        return char.isalpha() or char == "_"

    """ Source code scanning. """

    def match(self, char: str) -> bool:
        if self.atEnd() or self.peek() != char:
            return False
        self.advance()
        return True

    def matchGroup(self, chars: str) -> bool:
        clen = len(chars)
        if len(self.source) < self.current + clen or self.peekGroup(clen) != chars:
            return False
        for _ in chars:
            self.advance()
        return True

    def peekGroup(self, offset: int = 2) -> str:
        return self.source[self.current : self.current + offset]

    def peekNext(self) -> str:
        if self.atEnd():
            return "\0"
        return self.source[self.current + 1]

    def peek(self) -> str:
        return self.source[self.current]

    def advance(self) -> str:
        if self.peek() == "\n":
            self.currentrow += 1
            self.currentcol = 1
        else:
            self.currentcol += 1
        self.current += 1
        return self.source[self.current - 1]

    def atEnd(self) -> bool:
        return self.current >= len(self.source)

    @property
    def lexeme(self) -> str:
        return self.source[self.start : self.current]
