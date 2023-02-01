# Skiylia Interpreter, Used as an entrypoint to make Skiylia code work

import os
import sys

from Lexer import Lex
from Parser import Parse

class Skiylia:
    DEBUG = False

    def run(self, program_file: str) -> None:
        with open(program_file, "r") as f:
            program_contents = f.read()
        tokens = Lex(program_contents, self.DEBUG)
        bytecode = Parse(tokens, self.DEBUG)

    def entry_point(self, argv: list[str]) -> int:
        if "-d" in argv:
            argv.remove("-d")
            self.DEBUG = True
        
        if len(argv) == 0:
            print("Error: Must supply a filename.")
            return 1
        if not os.path.exists(argv[0]):
            print("Error: file does not exist.")
            return 2
        self.run(argv[0])
        return 0


if __name__ == "__main__":
    Skiylia().entry_point(sys.argv[1:])
