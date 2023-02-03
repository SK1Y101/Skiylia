# # Tests to verify the correct functioning of the Skiylia lexer

import pytest

from Parser import opcodes
from skiylia_errors import UnidentifiedCharacter, UnterminatedString

from .fixtures import parser  # isort:skip


class TestParserParses:
    """Test the parser generates the correct bytecode."""

    def test_debug(self, parser: parser, capsys) -> None:
        number1, number2, number3 = 1.4, 6.7, 8891
        parser(f"{number1}+{number2}/{number3}", True, False)
        assert capsys.readouterr().out.split("\n") == [
            "== test ==",
            f"{0:04d} {1:4d} {'OP_CONSTANT'.ljust(16)} {0:4d} '{float(number1)}'",
            f"{2:04d}    | {'OP_CONSTANT'.ljust(16)} {1:4d} '{float(number2)}'",
            f"{4:04d}    | {'OP_CONSTANT'.ljust(16)} {2:4d} '{float(number3)}'",
            f"{6:04d}    | {'OP_DIVIDE'.ljust(16)} ",
            f"{7:04d}    | {'OP_ADD'.ljust(16)} ",
            f"{8:04d}    | {'OP_RETURN'.ljust(16)} ",
            "",
        ]

    def test_parse_constant(self, parser: parser) -> None:
        bytecode = parser("1")
        assert bytecode == bytearray([opcodes.CONSTANT, 0, opcodes.RETURN])

    def test_parse_constant_fail(self, parser: parser) -> None:
        with pytest.raises(UnidentifiedCharacter):
            parser("1.2.3")
        with pytest.raises(UnidentifiedCharacter):
            parser(".1")

    def test_parse_comments_not_included(self, parser: parser) -> None:
        bytecode = parser("// comment here\n1+3")
        assert bytecode == bytearray(
            [opcodes.CONSTANT, 0, opcodes.CONSTANT, 1, opcodes.ADD, opcodes.RETURN]
        )

    def test_parse_string_fails(self, parser: parser) -> None:
        with pytest.raises(UnterminatedString):
            parser("'hello")

    def test_parse_arithmetic(self, parser: parser) -> None:
        bytecode = parser("1+2")
        assert bytecode == bytearray(
            [opcodes.CONSTANT, 0, opcodes.CONSTANT, 1, opcodes.ADD, opcodes.RETURN]
        )
        bytecode = parser("1-2")
        assert bytecode == bytearray(
            [opcodes.CONSTANT, 0, opcodes.CONSTANT, 1, opcodes.SUBTRACT, opcodes.RETURN]
        )
        bytecode = parser("1*2")
        assert bytecode == bytearray(
            [opcodes.CONSTANT, 0, opcodes.CONSTANT, 1, opcodes.MULTIPLY, opcodes.RETURN]
        )
        bytecode = parser("1/2")
        assert bytecode == bytearray(
            [opcodes.CONSTANT, 0, opcodes.CONSTANT, 1, opcodes.DIVIDE, opcodes.RETURN]
        )

    def test_parse_arithmetic_order_of_operation(self, parser: parser) -> None:
        bytecode = parser("4 - 3 * 7")
        assert bytecode == bytearray(
            [
                opcodes.CONSTANT,
                0,
                opcodes.CONSTANT,
                1,
                opcodes.CONSTANT,
                2,
                opcodes.MULTIPLY,
                opcodes.SUBTRACT,
                opcodes.RETURN,
            ]
        )
        bytecode = parser("4 / 3 + 7")
        assert bytecode == bytearray(
            [
                opcodes.CONSTANT,
                0,
                opcodes.CONSTANT,
                1,
                opcodes.DIVIDE,
                opcodes.CONSTANT,
                2,
                opcodes.ADD,
                opcodes.RETURN,
            ]
        )
