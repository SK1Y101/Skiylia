# Skiylia Interpreter, Used as an entrypoint to make Skiylia code work

import os
import sys

from Parser import Parser


class Skiylia:
    DEBUG = False
    SUPERDEBUG = False

    def run(self, program_file: str) -> None:
        with open(program_file, "r") as f:
            program_contents = f.read()
        parser = Parser(program_file, self.DEBUG)
        bytecode = parser.parseAll(program_contents)
        print(bytecode)

    def entry_point(self, argv: list[str]) -> int:
        if "-d" in argv:
            argv.remove("-d")
            self.DEBUG = True
        if "-dd" in argv:
            self.DEBUG = True
            self.SUPERDEBUG = True

        if len(argv) == 0:
            print("Error: Must supply a filename.")
            return 1
        if not os.path.exists(argv[0]):
            print("Error: file does not exist.")
            return 2

        if self.SUPERDEBUG:
            self.run(argv[0])
        else:
            try:
                self.run(argv[0])
            except Exception as e:
                print(e)
        return 0


if __name__ == "__main__":
    Skiylia().entry_point(sys.argv[1:])
