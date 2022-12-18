# Skiylia Interpreter, Used as an entrypoint to make Skiylia code work

import os
import sys

import lexer

def run(program_file: str) -> None:
    with open(program_file, "r") as f:
        program_contents = f.read()
    tokens = lexer.Lex(program_contents)
    print(tokens)

def entry_point(argv: sys.argv) -> int:
    if len(argv) == 0:
        print("Error: Must supply a filename.")
        return 1
    if not os.path.exists(argv[0]):
        print("Error: file does not exist.")
        return 2
    run(argv[-1])
    return 0

def target(*args) -> entry_point:
    return entry_point, None

if __name__ == "__main__":
    entry_point(sys.argv)