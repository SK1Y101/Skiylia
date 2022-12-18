# Skiylia Lexer, converts source code to recognised tokens

from lexer.token import Token

def Lex(program: str) -> list[Token]:
    lexer = Lexer(program)
    return lexer.lex()

class Lexer:
    def __init__(self, program: str) -> None:
        self.pos: int = 0
        self.row: int = 0
        self.column: int = 0
        self.source: str = program
        self.sourcelen: int = len(program)
    
    def lex(self) -> list[Token]:
        """Continue to parse source code until we complete the token stream."""
        self.tokens = []
        while not self.atEnd():
            token = self.scanToken()
            self.tokens.append(token)
        return self.tokens

    def scanToken(self) -> Token:
        """Fetch the next token in the source."""
        c = self.advance()
        return Token("None", c)
    
    def peek(self, offset: int = 0) -> str:
        if self.pos+offset <= self.sourcelen:
            return self.source[self.pos+offset]
        return "\0"

    def advance(self) -> str:
        self.pos += 1
        if self.atEnd():
            return "\0"
        return self.source[self.pos-1]
    
    def atEnd(self) -> bool:
        return self.pos >= self.sourcelen