# Skiylia Parser, converts tokenised code to bytecode

from Lexer import Lexer, Token
from skiylia_errors import error

from .grammar_rules import grammar
from .groups import Group
from .opcodes import OpCodes


def Parse(program: str, debug: bool = False) -> bytearray:
    parser = Parser("test", debug)
    return parser.parseAll(program)


class Parser(grammar):
    def __init__(self, name: str, debug: bool = False) -> None:
        self.debug = debug
        self.group = Group(name)
        self.pos = 0
        self.current: Token = None
        self.previous: Token = None
        self.panicMode = False
        self.hadError = False

    def parseAll(self, program: str) -> bytearray:
        self.lexer = Lexer(program, True)
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
        if not self.hadError:
            self.group.disasemble()

    def parsePrecedence(self, prec: int) -> None:
        pass

    """ Bytecode operations. """

    def emitBytes(self, byte1: int, byte2: int) -> None:
        self.emitByte(byte1)
        self.emitByte(byte2)

    def emitByte(self, byte: int) -> None:
        self.group.write(byte, self.previous.row, self.previous.col)

    def emitReturn(self) -> None:
        self.emitByte(OpCodes.RETURN)

    def emitConstant(self, value: float) -> None:
        self.emitBytes(OpCodes.CONSTANT, self.group.addConstant(value))

    """ Token operations. """

    def advance(self):
        self.previous = self.current
        while True:
            self.current = self.lexer.lex()
            if self.current.type != "ERROR":
                break
            self.errorAtCurrent()

    def consume(self, type: str, message: str):
        if self.current.type == type:
            self.advance()
            return
        self.errorAtCurrent(message)

    # def peek(self, offset: int = 0) -> str:
    #     if self.pos + offset >= self.sourcelen:
    #         return "\0"
    #     return self.source[self.pos + offset]

    # def match(self, char: str) -> bool:
    #     if self.peek() != char:
    #         return False
    #     self.advance()
    #     return True

    # def advance(self, offset: int = 1) -> str:
    #     self.pos += offset
    #     self.column += offset
    #     char = self.source[self.pos - offset]
    #     if char == "\n":
    #         self.temp = (self.row, self.column)
    #         self.row += 1
    #         self.column = 1
    #     return char

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
