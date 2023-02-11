# Tests to verify the correct functioning of the Skiylia virtual machine

import pytest

from .fixtures import virtual_machine  # isort:skip


class TestVmExecutes:
    def test_vm_debug(self, virtual_machine: virtual_machine, capsys) -> None:
        number1, number2 = 2, 1
        assert virtual_machine(f"{number1} + -{number2}", True) == 1
        assert capsys.readouterr().out.split("\n") == [
            "-- test --",
            f"{1:4d} {'NUMBER'.rjust(10)} '{number1}': {float(number1)}",
            f"   | {'PLUS'.rjust(10)} '+'",
            f"   | {'MINUS'.rjust(10)} '-'",
            f"   | {'NUMBER'.rjust(10)} '{number2}': {float(number2)}",
            f"   | {'EOF'.rjust(10)} '\\0'",
            "== test ==",
            f"{0:04d} {1:4d} {'OP_CONSTANT'.ljust(16)} {0:4d} '{float(number1)}'",
            f"{2:04d}    | {'OP_CONSTANT'.ljust(16)} {1:4d} '{float(number2)}'",
            f"{4:04d}    | {'OP_NEGATE'.ljust(16)} ",
            f"{5:04d}    | {'OP_ADD'.ljust(16)} ",
            f"{6:04d}    | {'OP_RETURN'.ljust(16)} ",
            "<< test >>",
            "",
            "[]",
            f"{0:04d} {'OP_CONSTANT'.ljust(16)} {0:4d} '{float(number1)}'",
            "",
            f"[{float(number1)}]",
            f"{2:04d} {'OP_CONSTANT'.ljust(16)} {1:4d} '{float(number2)}'",
            "",
            f"[{float(number1)}][{float(number2)}]",
            f"{4:04d} {'OP_NEGATE'.ljust(16)} ",
            "",
            f"[{float(number1)}][{-float(number2)}]",
            f"{5:04d} {'OP_ADD'.ljust(16)} ",
            "",
            f"[{float(number1) + -float(number2)}]",
            f"{6:04d} {'OP_RETURN'.ljust(16)} ",
            "",
        ]

    def test_vm_arithmetic(self, virtual_machine: virtual_machine) -> None:
        assert virtual_machine("1+2") == 3

    def test_vm_arithmetic_order_of_operations(
        self, virtual_machine: virtual_machine
    ) -> None:
        assert virtual_machine("2 - 6 * 3 / 4") == -2.5

    def test_vm_return_string(self, virtual_machine: virtual_machine) -> None:
        assert virtual_machine('"hello world!"') == "hello world!"

    def test_vm_unary_operations(self, virtual_machine: virtual_machine) -> None:
        assert virtual_machine("-2") == -2
        assert virtual_machine("+-2") == 2

    def test_vm_reach_eof(self, virtual_machine: virtual_machine) -> None:
        assert virtual_machine("") == None
