# Skiylia base type used to represent numbers

class Number(float):
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value
    
    def __repr__(self) -> str:
        return f"{self.value:g}"

class NumberGroup:
    def __init__(self) -> None:
        self.count = 0
        self.memory: list[Number] = []
    
    def write(self, value: Number) -> None:
        self.memory.append(value)
        self.count += 1
        return self.count - 1
    
    def read(self, idx: int) -> Number:
        return self.memory[idx ]
    
    def free(self) -> None:
        self.__init__()