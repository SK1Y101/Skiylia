import nox

directories = ["src", "tests"]

format_dirs = ["noxfile.py"] + directories


@nox.session
def format(session: nox.session) -> None:
    """Reformat python files."""
    session.install("black", "isort")
    session.run(
        "isort",
        "--profile",
        "black",
        "--check-only",
        *format_dirs,
    )
    session.run("black", *format_dirs)


@nox.session
def lint(session: nox.session) -> None:
    """Lint all python files."""
    session.install("flake8", "isort")
    session.run(
        "isort",
        "--profile",
        "black",
        "--check-only",
        *format_dirs,
    )
    session.run("flake8", *format_dirs, "--max-line-length", "88")


@nox.session
def mypy(session: nox.session) -> None:
    """Check python files for type violations."""
    dirs = []
    for dire in directories:
        dirs.extend(["-p", dire])

    session.install("mypy")
    session.run("mypy", *dirs)


@nox.session
def tests(session: nox.session) -> None:
    """Run the test suite."""
    session.install("pytest")
    session.run("pytest", "tests")
