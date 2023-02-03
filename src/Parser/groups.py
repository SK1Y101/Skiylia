# Skiylia group class, used to represent small groupings of bytecode

from typing import Any

from .opcodes import opcodes


class NumberGroup:
    def __init__(self) -> None:
        self.count = 0
        self.memory: list[float] = []

    def write(self, value: float) -> int:
        self.memory.append(value)
        self.count += 1
        return self.count - 1

    def read(self, idx: int) -> float:
        return self.memory[idx]

    def free(self) -> None:
        self.count = 0
        self.memory.clear()


class Group:
    def __init__(self, name: str) -> None:
        self.name = name
        self.code = bytearray()
        self.constants = NumberGroup()
        self.lines: list[int] = []
        self.cols: list[int] = []
        self.count = 0
        self.dis = 0

    def write(self, byte: int, line: int, col: int) -> int:
        self.count += 1
        self.code.append(byte)
        self.lines.append(line)
        self.cols.append(col)
        return self.count - 1

    def read(self, idx: int) -> Any:
        return self.code[idx]

    def free(self) -> None:
        self.count = 0
        self.code.clear()
        self.lines.clear()
        self.cols.clear()

    def toByteCode(self) -> bytearray:
        return self.code

    """= ==== DEBUGGING ===== """

    def disasemble(self) -> None:
        print(f"== {self.name} ==")
        offset, lastline = 0, 0
        while offset < self.count:
            line = self.lines[offset]
            idx, op, text, offset = self.disassembleInstruction(offset)
            print(
                f"{idx:04d}",
                "   |" if line == lastline else f"{line:4d}",
                op.ljust(16),
                text,
            )
            lastline = line

    def disassembleInstruction(self, offset: int) -> tuple[int, str, str, int]:
        opcode = self.read(offset)
        match opcode:
            case opcodes.RETURN:
                return self.simpleInstruction("OP_RETURN", offset)
            case opcodes.CONSTANT:
                return self.constantInstruction("OP_CONSTANT", offset)
            # Binary operations
            case opcodes.ADD:
                return self.simpleInstruction("OP_ADD", offset)
            case opcodes.SUBTRACT:
                return self.simpleInstruction("OP_SUBTRACT", offset)
            case opcodes.MULTIPLY:
                return self.simpleInstruction("OP_MULTIPLY", offset)
            case opcodes.DIVIDE:
                return self.simpleInstruction("OP_DIVIDE", offset)
            case _:
                return self.unknownInstruction(opcode, offset)

    def constantInstruction(
        self, opcode: str, offset: int
    ) -> tuple[int, str, str, int]:
        constptr = self.read(offset + 1)
        constant = f"{constptr} '{self.constants.read(constptr)}'"
        return offset, opcode, constant, offset + 2

    def simpleInstruction(self, opcode: str, offset: int) -> tuple[int, str, str, int]:
        return offset, opcode, "", offset + 1

    def unknownInstruction(self, opcode: Any, offset: int) -> tuple[int, str, str, int]:
        return offset, "Unknown opcode", opcode, offset + 1

    """ ===== OPERATIONS ON THE GROUP ===== """

    def addConstant(self, value: float) -> int:
        return self.constants.write(value)
