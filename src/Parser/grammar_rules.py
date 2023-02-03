# Abstraction of the Skiylia grammar
from typing import Callable

from .opcodes import opcodes


class parseRule:
    def __init__(
        self, prefix: Callable | None, infix: Callable | None, precedence: int
    ) -> None:
        self.prefix = prefix
        self.infix = infix
        self.precedence = precedence


class grammar:
    def __init__(self):
        """Precedence."""

        self.PREC_NONE = 0
        self.PREC_TERM = 1
        self.PREC_FACTOR = 2
        self.PREC_PRIMARY = 3

        """ Rules mapping. """

        self.RULES = {
            # special
            "EOF": parseRule(None, None, self.PREC_NONE),
            "ERROR": parseRule(None, None, self.PREC_NONE),
            "SPACE": parseRule(None, None, self.PREC_NONE),
            # symbols
            "MINUS": parseRule(None, self.binary, self.PREC_TERM),
            "PLUS": parseRule(None, self.binary, self.PREC_TERM),
            "SLASH": parseRule(None, self.binary, self.PREC_FACTOR),
            "STAR": parseRule(None, self.binary, self.PREC_FACTOR),
            # literals
            "NUMBER": parseRule(self.number, None, self.PREC_NONE),
            # keywords
        }

    def getRule(self, tokenType: str) -> parseRule:
        return self.RULES[tokenType]

    """ Structures. """

    def expression(self) -> None:
        self.parsePrecedence(1)  # type: ignore

    def binary(self) -> None:
        op = self.previous.type  # type: ignore
        rule = self.getRule(op)
        self.parsePrecedence(rule.precedence + 1)  # type: ignore

        match op:
            case "PLUS":
                self.emitByte(opcodes.ADD)  # type: ignore
            case "MINUS":
                self.emitByte(opcodes.SUBTRACT)  # type: ignore
            case "STAR":
                self.emitByte(opcodes.MULTIPLY)  # type: ignore
            case "SLASH":
                self.emitByte(opcodes.DIVIDE)  # type: ignore

    """ Raw Data types. """

    def number(self) -> None:
        value = self.previous.literal  # type: ignore
        self.emitConstant(value)  # type: ignore
