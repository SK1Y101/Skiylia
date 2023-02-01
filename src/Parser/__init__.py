# Skiylia Parser, converts tokenised code to bytecode

from Lexer import Token

from .opcodes import OpCodes
from .groups import Group
from .Types import Number


def Parse(program: list[Token], debug: bool = False) -> list[int]:
    parser = Parser(program, debug)
    return parser.parseAll()


class Parser:
    def __init__(self, program: list[Token], debug: bool = False) -> None:
        self.program = program
        self.debug = debug

    def parse(self) -> int:
        pass

    def parseAll(self) -> list[int]:
        group = Group("test")
        constant = group.addConstant(Number.Number(56))
        group.write(OpCodes.CONSTANT, 123)
        group.write(constant, 123)
        group.write(OpCodes.RETURN, 123)
        if self.debug:
            group.disasemble()
        return group.toByteCode()
