# Fixtures used for the skiylia test suite

import sys
import pytest

sys.path.append("src")

from Lexer import Lex, Token
from Parser import Parse


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

@pytest.fixture
def parser():
    return Parse

@pytest.fixture
def lexer():
    return Lex


@pytest.fixture
def decompose():
    return decomposeLexer
