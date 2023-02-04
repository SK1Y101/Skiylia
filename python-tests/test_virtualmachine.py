# Tests to verify the correct functioning of the Skiylia virtual machine

import pytest

from .fixtures import virtual_machine  # isort:skip


class TestVmExecutes:
    def test_vm_arithmetic(self, virtual_machine: virtual_machine) -> None:
        assert virtual_machine("1+2") == 3

    def test_vm_arithmetic_order_of_operations(
        self, virtual_machine: virtual_machine
    ) -> None:
        assert virtual_machine("2 - 6 * 3 / 4") == -2.5
