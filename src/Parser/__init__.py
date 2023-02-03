# Skiylia Parser, converts tokenised code to bytecode

from Lexer import Lexer, Token
from skiylia_errors import error

from .grammar_rules import grammar
from .groups import Group
from .opcodes import opcodes


def Parse(program: str, debug: bool = False, lexerDebug: bool = False) -> bytearray:
    parser = Parser("test", debug)
    return parser.parseAll(program, lexerDebug)


class Parser(grammar):
    def __init__(self, name: str, debug: bool = False) -> None:
        super().__init__()
        self.debug = debug
        self.group = Group(name)
        self.pos = 0
        self.current: Token = None
        self.previous: Token = None
        self.panicMode = False
        self.hadError = False

    def parseAll(self, program: str, lexerDebug: bool | None = None) -> bytearray:
        self.lexer = Lexer(program, self.debug if lexerDebug is None else lexerDebug)
        while not self.lexer.atEnd():
            self.parse()
        if self.debug:
            self.group.disasemble()
        return self.group.toByteCode()

    def parse(self) -> bool:
        """Parse the token into bytecode."""
        self.advance()
        self.expression()
        self.consume("EOF", "Expected end of expression.")
        self.endParsing()
        return not self.hadError

    def endParsing(self) -> None:
        self.emitReturn()
        if self.hadError:
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

    def emitBytes(self, byte1: int, byte2: int) -> None:
        self.emitByte(byte1)
        self.emitByte(byte2)

    def emitByte(self, byte: int) -> None:
        self.group.write(byte, self.previous.row, self.previous.col)

    def emitReturn(self) -> None:
        self.emitByte(opcodes.RETURN)

    def emitConstant(self, value: float) -> None:
        self.emitBytes(opcodes.CONSTANT, self.group.addConstant(value))

    """ Token operations. """

    def advance(self) -> None:
        self.previous = self.current
        while not self.lexer.atEnd():
            self.current = self.lexer.lex(ignore_comment=True)
            if self.current.type != "ERROR":
                break
            self.errorAtCurrent()

    def consume(self, type: str, message: str) -> None:
        if self.current.type == type:
            self.advance()
            return
        self.errorAtCurrent(message)

    def errorAtCurrent(self, message: str = "") -> None:
        self.errorAt(self.current, message)

    def error(self, message: str) -> None:
        self.errorAt(self.previous, message)

    def errorAt(self, token: Token, message: str) -> None:
        if self.panicMode:
            return
        self.panicMode = True
        if token.type == "ERROR":
            self.exception(error().reverse(token.literal), token, message)
        self.exception(error().reverse(), token, message)

    def exception(
        self,
        exception,
        token: Token,
        message: str = "",
    ) -> None:
        if message:
            raise exception(token.row, token.col, message)
        raise exception(token.row, token.col, token.lexeme)