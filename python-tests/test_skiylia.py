# Tests to verify the correct functioning of the Skiylia entrypoint

import os

import pytest

from skiylia import Skiylia

from .fixtures import skiylia, skiylia_args


class TestSkiyliaArgs:
    def test_skiylia_help(self, skiylia_args: skiylia_args, capsys) -> None:
        with pytest.raises(SystemExit):
            skiylia_args(["-h"])
        out, _ = capsys.readouterr()
        assert out == "\n".join(
            [
                f"usage: {Skiylia.name} [-h] [-d] [-v] file",
                "",
                f"{Skiylia.name} Interprter version {Skiylia.Version.version}, Read more at",
                f"{Skiylia.url}.",
                "",
                "positional arguments:",
                f"  file           {Skiylia.name} file to execute",
                "",
                "options:",
                "  -h, --help     show this help message and exit",
                "  -d, --debug    increase output debug level",
                f"  -v, --version  return the currently installed {Skiylia.name} version",
                "",
            ]
        )

    def test_skiylia_arguments_errors(self, skiylia_args: skiylia_args) -> None:
        with pytest.raises(TypeError):
            skiylia_args()
        with pytest.raises(SystemExit):
            skiylia_args([])
        with pytest.raises(SystemExit):
            skiylia_args(["-d"])


class TestSkiyliaExecution:
    def test_skiylia_file_not_found(self, skiylia: skiylia) -> None:
        invalid_file = "test.py"
        assert (
            skiylia(invalid_file, 1).out
            == "Skiylia encountered InvalidFileError:\n"
            + f"'{invalid_file}' is not a valid Skiylia file.\n"
        )
        file_not_found = "non_existent_file.skiy"
        assert (
            skiylia(file_not_found, 1).out
            == "Skiylia encountered FileNotFoundError:\n"
            + f"'{file_not_found}' does not exist.\n"
        )

    def test_skiylia_debug_levels(self, skiylia: skiylia) -> None:
        file_not_found = "non_existent_file.skiy"

        debug = [skiylia(file_not_found, x).out for x in range(0, 3)]

        assert debug == [
            # level 0
            "Skiylia encountered FileNotFoundError:\n"
            + "Re-execute with debug enabled.\n",
            # level 1
            "Skiylia encountered FileNotFoundError:\n"
            + f"'{file_not_found}' does not exist.\n",
            # level 2
            "Skiylia encountered FileNotFoundError:\n"
            + "Traceback (most recent call last):\n"
            + f'  File "{os.getcwd()}/src/skiylia.py", line 87, in entry_point\n'
            + "    raise FileNotFoundError(f\"'{program_name}' does not exist.\")\n"
            + f"FileNotFoundError: '{file_not_found}' does not exist.\n",
        ]

    def test_skiylia_arithmetic(self, skiylia: skiylia, tmp_path) -> None:
        content = "1+2"

        tmp_file = tmp_path / "aithmetic_test.skiy"
        tmp_file.write_text(content)
        assert tmp_file.read_text() == content
        fname = str(tmp_file)

        execution = skiylia(fname).out
        assert execution == f"{float(3)}\n"

    def test_skiylia_string(self, skiylia: skiylia, tmp_path) -> None:
        string = "hello world!"
        content = f"'{string}'"

        tmp_file = tmp_path / "string_test.skiy"
        tmp_file.write_text(content)
        assert tmp_file.read_text() == content
        fname = str(tmp_file)

        execution = skiylia(fname).out
        assert execution == f"{string}\n"
