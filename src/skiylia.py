# Skiylia Interpreter, Used as an entrypoint to make Skiylia code work

import os
import sys

from lexer import Lex


def run(program_file: str) -> None:
    with open(program_file, "r") as f:
        program_contents = f.read()
    tokens = Lex(program_contents)
    print(*tokens, sep=", ")


def entry_point(argv: list[str]) -> int:
    if len(argv) == 0:
        print("Error: Must supply a filename.")
        return 1
    if not os.path.exists(argv[0]):
        print("Error: file does not exist.")
        return 2
    run(argv[0])
    return 0


if __name__ == "__main__":
    entry_point(sys.argv[1:])
