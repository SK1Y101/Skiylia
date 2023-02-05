# Tests to verify the correct functioning of the Skiylia entrypoint

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
                f"usage: {Skiylia.name} [-h] [-d] file",
                "",
                Skiylia.description,
                "",
                "positional arguments:",
                "  file         Skiylia file to execute.",
                "",
                "options:",
                "  -h, --help   show this help message and exit",
                "  -d, --debug  increase output debug level.",
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
