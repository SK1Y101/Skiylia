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

    """Precedence."""

    PREC_NONE = 0
    PREC_TERM = 1  # + -
    PREC_FACTOR = 2  # * /
    PREC_UNARY = 3  # -a +a
    PREC_PRIMARY = 4

    def __init__(self):
        """Rules mapping."""

        self.RULES = {
            # special
            "EOF": parseRule(None, None, self.PREC_NONE),
            "ERROR": parseRule(None, None, self.PREC_NONE),
            "SPACE": parseRule(None, None, self.PREC_NONE),
            # symbols
            "MINUS": parseRule(self.unary, self.binary, self.PREC_TERM),
            "PLUS": parseRule(self.unary, self.binary, self.PREC_TERM),
            "SLASH": parseRule(None, self.binary, self.PREC_FACTOR),
            "STAR": parseRule(None, self.binary, self.PREC_FACTOR),
            # literals
            "NUMBER": parseRule(self.number, None, self.PREC_NONE),
            "STRING": parseRule(self.string, None, self.PREC_NONE),
            "INTERPOLATION": parseRule(self.interpolation, None, self.PREC_NONE),
            "IDENTIFIER": parseRule(None, None, self.PREC_NONE),
            # keywords
        }

    def getRule(self, tokenType: str) -> parseRule:
        return self.RULES[tokenType]

    """ Structures. """

    def expression(self) -> None:
        self.parsePrecedence(1)  # type: ignore

    def interpolation(self) -> None:
        self.string()
        self.expression()
        self.consume("STRING", "Expected end of string interpolation.")  # type: ignore
        self.emitByte(opcodes.ADD)  # type: ignore

    def unary(self) -> None:
        op = self.previous.type  # type: ignore
        self.parsePrecedence(self.PREC_UNARY)  # type: ignore

        match op:
            case "MINUS":
                self.emitByte(opcodes.NEGATE)  # type: ignore
            case "PLUS":
                self.emitByte(opcodes.POSIGATE)  # type: ignore

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

    def string(self) -> None:
        value = self.previous.lexeme  # type: ignore
        self.emitConstant(value)  # type: ignore
