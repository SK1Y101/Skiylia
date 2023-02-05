import os
import re
import sys

import nox

sys.path.insert(0, os.path.abspath("src"))

# run mypy on these
directories = ["src"]
# additionally run flake8 on these
lint_dirs = ["noxfile.py"] + directories
# and run black and isort on these
format_dirs = ["python-tests"] + lint_dirs

nox.options.sessions = [
    "black",
    "isort",
    "lint",
    "mypy",
    "tests",
]
nox.options.stop_on_first_error = True


@nox.session(tags=["format", "lint"])
def black(session: nox.session) -> None:
    """Reformat python files."""
    session.install("black")
    session.run("black", *format_dirs)


@nox.session(tags=["format", "lint"])
def isort(session: nox.session) -> None:
    session.install("isort")
    session.run(
        "isort",
        "--profile",
        "black",
        *format_dirs,
    )

    skiyfile = "src/skiylia.py"
    build = session.run(
        "git", "rev-list", "--count", "HEAD", silent=True, external=True
    )
    buildnum = int(build[:-1])

    with open(skiyfile, "r") as skiyliafile:
        content = skiyliafile.read()

    skiyliabuild = int(
        re.search(
            r"\d+",
            re.search(
                r"build = \d+", [x for x in content.split("\n") if "build = " in x][0]
            ).group(),
        ).group()
    )

    if skiyliabuild != buildnum:
        content = content.replace(f"build = {skiyliabuild}", f"build = {buildnum}")
        with open(skiyfile, "w") as skiyliafile:
            skiyliafile.write(content)
        session.log(f"Skiylia build updated to {buildnum}")


@nox.session(tags=["lint"])
def lint(session: nox.session) -> None:
    """Lint all python files."""
    session.install("flake8")
    session.run(
        "flake8", *lint_dirs, "--max-line-length", "88", "--extend-ignore", "E203"
    )
    session.debug("Checking skiylia versioning information")

    from skiylia import Skiylia

    build = session.run(
        "git", "rev-list", "--count", "HEAD", silent=True, external=True
    )
    buildnum = int(build[:-1])
    if buildnum != Skiylia.Version.build:
        session.error(f"{Skiylia.name} build incorrect (should be '{buildnum}')")
    if Skiylia.Version.ident not in ["pre-alpha", "alpha", "beta", ""]:
        session.error(
            f"{Skiylia.name} stage incorrect, {Skiylia.Version.ident} invalid"
        )


@nox.session(tags=["lint"])
def mypy(session: nox.session) -> None:
    """Check python files for type violations."""
    dirs = []
    for dire in directories:
        dirs.extend(["-p", dire])

    session.install("mypy")
    session.run("mypy", *dirs, "--ignore-missing-imports")


@nox.session(tags=["test"])
def tests(session: nox.session) -> None:
    """Run the python test suite."""
    session.install("pytest")
    session.install("coverage")
    session.run(
        "coverage",
        "run",
        "-m",
        "pytest",
        "python-tests",
        "--import-mode=importlib",
        "--durations=10",
        "-v",
    )
    session.run("coverage", "report", "-m")


@nox.session
def skiytests(session: nox.session) -> None:
    """Run the skiylia test suite (Non-functional for now)"""
    # session.run("python3 src/skiylia.py")
