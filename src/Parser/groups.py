# Skiylia group class, used to represent small groupings of bytecode

from .Types import Number
from .opcodes import OpCodes

class Group:
    def __init__(self, name: str) -> None:
        self.name = name
        self.code = bytearray()
        self.constants = Number.NumberGroup()
        self.lines = list()
        self.count = 0

    def write(self, byte: int, line: int) -> None:
        self.count += 1
        self.code.append(byte)
        self.lines.append(line)
        return self.count - 1
    
    def read(self, idx: int) -> Number:
        return self.code[idx]

    def free(self) -> None:
        self.__init__()
    
    def toByteCode(self) -> list[int]:
        return self.code

    """ Debug information. """

    def disasemble(self) -> str:
        print(f"== {self.name} ==")
        offset, lastline = 0, 0
        while offset < self.count:
            line = self.lines[offset]
            idx, op, text, offset = self.disassembleInstruction(offset)
            print(f"{idx:04d}",
                "   |" if line == lastline else f"{line:4d}",
                op.ljust(16),
                text)
            lastline = line

    def disassembleInstruction(self, offset: int) -> tuple[int, str, str, int]:
        opcode = self.read(offset)
        match opcode:
            case OpCodes.RETURN:
                return self.simpleInstruction("OP_RETURN", offset)
            case OpCodes.CONSTANT:
                return self.constantInstruction("OP_CONSTANT", offset)
            case _:
                return self.unknownInstruction(opcode, offset)

    def constantInstruction(self, opcode: str, offset: int) -> tuple[int, str, str, int]:
        constptr = self.read(offset + 1)
        constant = f"{constptr} '{self.constants.read(constptr)}'"
        return offset, opcode, constant, offset + 2

    def simpleInstruction(self, opcode: str, offset: int) -> tuple[int, str, str, int]:
        return offset, opcode, "", offset + 1
    
    def unknownInstruction(self, opcode: str, offset: int) -> tuple[int, str, str, int]:
        return offset, "Unknown opcode", opcode, offset + 1
    
    """ Parsing operations. """
    
    def addConstant(self, value: Number.Number) -> None:
        return self.constants.write(value)