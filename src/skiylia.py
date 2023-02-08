#!/usr/bin/env python3
# Skiylia Interpreter, Used as an entrypoint to make Skiylia code work

import argparse
import os
import sys
import traceback

from skiylia_errors import InvalidFileError
from VirtualMachine import Vm, vmresult


class Skiylia:
    class Version:
        # Introduce new features that are not backwards compatible
        major = 0
        # Introduce new features that are backwards compatible
        minor = 1
        # Fix bugs or issues (backwards compatible by definition)
        patch = 0
        # Build number (commits since initial tracks approximate age)
        build = 144
        # Additional identifiers (ie: alpha)
        ident = "pre-alpha"

        # Full version representation
        version = ".".join(
            [
                f"{major:d}",
                f"{minor:d}",
                f"{patch:d}",
                f"{build:d}",
            ]
        ) + (f"-{ident}" if ident else "")

    # description
    name = "Skiylia"
    url = "https://skiylia.readthedocs.io"
    description = f"{name} Interprter version {Version.version}, Read more at {url}."
    # interpreter-specific
    DEBUG = 0
    valid_extensions = [".skiy"]

    def parse_args(self, args: list[str]):
        parser = argparse.ArgumentParser(prog=self.name, description=self.description)
        parser.add_argument("file", help=f"{self.name} file to execute")
        parser.add_argument(
            "-d",
            "--debug",
            help="increase output debug level",
            action="count",
            default=0,
        )
        parser.add_argument(
            "-v",
            "--version",
            help=f"return the currently installed {self.name} version",
            action="version",
            version=f"{self.name} {self.Version.version}",
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

            if os.path.splitext(program_name)[1] not in self.valid_extensions:
                raise InvalidFileError(
                    f"'{program_name}' is not a valid {self.name} file."
                )
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
            print(f"{self.name} encountered {e.__class__.__name__}:\n{errtext}")
        return 0


if __name__ == "__main__":
    skiylia = Skiylia()
    skiylia.entry_point(skiylia.parse_args(sys.argv[1:]))
