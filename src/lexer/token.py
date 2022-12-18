# Skiylia Token class, used to symbolically represent chunks of source code

class Token:
    def __init__(self, type: str, lexeme: str, literal: any = None, col: int = 0, row: int = 0) -> None:
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.col = col
        self.row = row
    
    def __repr__(self) -> str:
        return f"{self.type} {self.lexeme} {self.literal}"