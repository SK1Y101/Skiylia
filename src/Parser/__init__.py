# Skiylia Parser, converts tokenised code to bytecode

from typing import Type

from Lexer import Lexer, Token
from skiylia_errors import SkiyliaError, error

from .grammar_rules import grammar
from .groups import Group
from .opcodes import opcodes


class Parser(grammar):
    def __init__(self, debug: bool = False) -> None:
        super().__init__()
        self.debug = debug
        self.pos = 0
        self.current: Token = None
        self.previous: Token = None
        self.panicMode = False
        self.hadError = False
        self.errors: list[Type[SkiyliaError]] = []

    def parse(self, program: str, group: Group) -> bool:
        """Parse the token into bytecode."""
        self.lexer = Lexer(program, self.debug)
        self.group = group
        if self.debug:
            print(f"-- {self.group.name} --")

        self.advance()
        self.expression()
        self.consume("EOF", "Expected end of expression.", error.INCOMPLETEEXPRESSION)

        self.endParsing()
        return not self.hadError

    def endParsing(self) -> None:
        self.emitReturn()
        if not self.hadError and self.debug:
            self.group.disasemble()

    def parsePrecedence(self, precedence: int) -> None:
        self.advance()
        prefixRule = self.getRule(self.previous.type).prefix
        if not prefixRule:
            self.error("Expected expression.")
            return

        prefixRule()

        while precedence <= self.getRule(self.current.type).precedence:
            self.advance()
            infixRule = self.getRule(self.previous.type).infix
            if infixRule:
                infixRule()

    """ Bytecode operations. """

    def emitByte(self, byte: int) -> None:
        self.group.write(byte, self.previous.row, self.previous.col)

    def emitBytes(self, byte1: int, byte2: int) -> None:
        self.emitByte(byte1)
        self.emitByte(byte2)

    def emitReturn(self) -> None:
        self.emitByte(opcodes.RETURN)

    def emitConstant(self, value: float) -> None:
        idx = self.group.addConstant(value)
        if idx < 256:
            self.emitBytes(opcodes.CONSTANT, idx)
        else:
            self.emitBytes(opcodes.CONSTANT_LONG, idx & 0xFF)
            self.emitBytes((idx >> 8) & 0xFF, (idx >> 16) & 0xFF)

    """ Token operations. """

    def advance(self) -> None:
        self.previous = self.current
        while not self.lexer.atEnd():
            self.current = self.lexer.lex(ignore_comment=True)
            if self.current.type != "ERROR":
                break
            self.errorAtCurrent()

    def consume(self, type: str, message: str, errcode: int = 0) -> None:
        if self.current.type == type:
            self.advance()
            return
        self.errorAtCurrent(message, errcode)

    def errorAtCurrent(self, message: str = "", errcode: int = 0) -> None:
        self.errorAt(self.current, message, errcode)

    def error(self, message: str, errcode: int = 0) -> None:
        self.errorAt(self.previous, message, errcode)

    def errorAt(self, token: Token, message: str, errcode: int = 0) -> None:
        if self.panicMode:
            return
        self.panicMode = True
        if token.type == "ERROR":
            self.exception(error().reverse(token.literal), token, message)
        else:
            self.exception(error().reverse(errcode), token, message)
        self.hadError = True

    def exception(
        self,
        exception,
        token: Token,
        message: str = "",
    ) -> None:
        exc = exception(token.row, token.col, message if message else token.lexeme)
        self.errors.append(exc)
        print(exc)
