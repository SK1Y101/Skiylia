# Fixtures used for the skiylia test suite

import sys

import pytest

sys.path.append("src")

from skiylia import Skiylia

from Lexer import Lexer, Token  # isort:skip
from Parser import Parser, Group  # isort:skip
from VirtualMachine import Vm  # isort: skip


class decomposedLexer:
    def __init__(self, program: str) -> None:
        self.types: list[str] = []
        self.tokens: list[Token] = []
        self.lexemes: list[str] = []
        self.literals: list[str] = []
        self.program = program

    def lex(self):
        self.tokens = Lex(self.program)
        for token in self.tokens:
            self.types.append(token.type)
            self.lexemes.append(token.lexeme)
            self.literals.append(token.literal)
        return self


def decomposeLexer(program: str) -> decomposedLexer:
    lexer = decomposedLexer(program)
    return lexer.lex()


def execute(program: str, debug: bool = False) -> None:
    vm = Vm(debug)
    vm.interpret(program, "test")
    return vm.final_state


def Parse(program: str, debug: bool = False) -> bytearray:
    parser = Parser(debug)
    group = Group("test")
    if not parser.parse(program, group):
        return parser.errors
    return group.toByteCode()


def Lex(program: str, debug: bool = False) -> list[Token]:
    lexer = Lexer(program, debug)
    tokens: list[Token] = []
    while not lexer.atEnd():
        tokens.append(lexer.lex())
    return tokens


@pytest.fixture
def skiylia_args():
    skiylia = Skiylia()
    return skiylia.parse_args


@pytest.fixture
def skiylia(capsys):
    def execute_code(program_name: str, debug: int = 0):
        skiylia = Skiylia()
        args = [program_name]
        match debug:
            case 1:
                args.append("-d")
            case 2:
                args.append("-dd")
        skiylia.entry_point(skiylia.parse_args(args))
        return capsys.readouterr()

    return execute_code


@pytest.fixture
def virtual_machine():
    return execute


@pytest.fixture
def parser():
    return Parse


@pytest.fixture
def lexer():
    return Lex


@pytest.fixture
def decompose():
    return decomposeLexer
