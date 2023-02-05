#!/usr/bin/env python3
# Skiylia Interpreter, Used as an entrypoint to make Skiylia code work

import argparse
import os
import sys
import traceback

from skiylia_errors import InvalidFileError, UnsuppliedFileError
from VirtualMachine import Vm, vmresult


class Skiylia:
    DEBUG = 0
    name = "Skiylia"
    version = "0.0.1"
    url = "https://skiylia.readthedocs.io"
    description = f"{name} Interprter version {version}. Read more at {url}."

    valid_extensions = [".skiy"]

    def parse_args(self, args: list[str]):
        parser = argparse.ArgumentParser(prog=self.name, description=self.description)
        parser.add_argument("file", help="Skiylia file to execute.")
        parser.add_argument(
            "-d",
            "--debug",
            help="increase output debug level.",
            action="count",
            default=0,
        )
        return parser.parse_args(args)

    def open_file(self, program_file: str) -> str:
        with open(program_file, "r") as f:
            return f.read()

    def run(self, program: str, env_name: str) -> None:
        vm = Vm(self.DEBUG)
        result = vm.interpret(program, env_name)

        if result == vmresult.INTERPRET_OK:
            print(vm.final_state)

        vm.free()

    def entry_point(self, args) -> int:
        self.DEBUG = args.debug

        try:
            program_name = args.file

            if not program_name:
                raise UnsuppliedFileError("Must supply a file.")
            if os.path.splitext(program_name)[1] not in self.valid_extensions:
                raise InvalidFileError(f"'{program_name}' is not a valid skiylia file.")
            if not os.path.exists(program_name):
                raise FileNotFoundError(f"'{program_name}' does not exist.")

            self.run(self.open_file(program_name), program_name)
        except Exception as e:
            # all hell breaks loose on superdebug
            if self.DEBUG > 1:
                errtext = traceback.format_exc()[:-1]
            # handle python errors nicely
            elif self.DEBUG:
                errtext = str(e)
            else:
                errtext = "Re-execute with debug enabled."
            print(f"Skiylia interpreter encountered {e.__class__.__name__}:\n{errtext}")
        return 0


if __name__ == "__main__":
    skiylia = Skiylia()
    skiylia.entry_point(skiylia.parse_args(sys.argv[1:]))
