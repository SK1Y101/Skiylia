# Skiylia Virtual machine, runs skiylia bytecode

from typing import Any

from Parser import Group, Parser, opcodes


class vmresult:
    INTERPRET_OK = 1
    INTERPRET_COMPILE_ERROR = 2
    INTERPRET_RUNTIME_ERROR = 3


class Vm:
    def __init__(self, debug: bool = False) -> None:
        self.group: Group = None
        self.ip: int = 0
        self.debug = debug
        self.stack: list[Any] = []

    def free(self) -> None:
        self.group = None
        self.ip = 0
        self.stack = []

    def interpret(self, program: str, program_name: str) -> int:
        group = Group(program_name)
        parser = Parser(self.debug)
        if not parser.parse(program, group):
            return vmresult.INTERPRET_COMPILE_ERROR

        self.group = group
        self.ip = 0
        result = self.run()

        return result

    def run(self) -> int:
        if self.debug:
            print(f"<< {self.group.name} >>")
        while True:
            if self.debug:
                stack = "".join([f"[{slot}]" for slot in self.stack])
                print(f"\n{stack if stack else '[]'}")
                self.group.disassembleOne(self.ip)

            instruction = self.readByte()
            match instruction:
                case opcodes.RETURN:
                    print(self.pop())
                    return vmresult.INTERPRET_OK
                case opcodes.CONSTANT:
                    constant = self.readConstant()
                    self.push(constant)
                case opcodes.ADD:
                    self.BINARY_OP("+")
                case opcodes.SUBTRACT:
                    self.BINARY_OP("-")
                case opcodes.MULTIPLY:
                    self.BINARY_OP("*")
                case opcodes.DIVIDE:
                    self.BINARY_OP("/")

    """ Stack operations. """

    def push(self, value: Any) -> None:
        self.stack.append(value)

    def pop(self) -> Any:
        return self.stack.pop()

    def BINARY_OP(self, op: str) -> None:
        b = self.pop()
        a = self.pop()
        match op:
            case "+":
                self.push(a + b)
            case "-":
                self.push(a - b)
            case "*":
                self.push(a * b)
            case "/":
                self.push(a / b)

    """ Bytecode operations. """

    def readByte(self, idx: int | None = None) -> int:
        self.ip += 1
        return self.group.read(self.ip - 1)

    def readConstant(self, idx: int | None = None) -> float:
        const = self.readByte(self.ip)
        return self.group.constants.read(const)
