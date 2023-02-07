import argparse
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

nox.options.sessions = ["black", "isort", "lint", "mypy", "tests"]
nox.options.stop_on_first_error = True


def parse_args(session):
    parser = argparse.ArgumentParser(description="Skiylia nox arguments")
    parser.add_argument(
        "--newcommit",
        help="bump the build number, used if about to push a new commit.",
        action="store_true",
        default=False,
    )
    parser.add_argument(
        "--last_ver", type=str, help="manually supply previous version", nargs="?"
    )
    parser.add_argument(
        "--debug",
        help="increase output debug level",
        action="store_true",
        default=False,
    )
    return parser.parse_args(args=session.posargs)


def fetch_last_release(session) -> str:
    try:
        last_release_ver = session.run(
            "git", "describe", "--abbrev=0", silent=True, external=True
        )
        return re.search(r"\d+\.\d+\.\d+", last_release_ver[:-1]).group()
    except Exception:
        return "0.0.0"


def fetch_build_number(session) -> str:
    return int(
        session.run(
            "git", "rev-list", "v0.0.0..HEAD", "--count", silent=True, external=True
        )[:-1]
    )


@nox.session(tags=["format", "lint"])
def black(session: nox.session) -> None:
    """Reformat python files."""
    session.install("black")
    session.run("black", *format_dirs)


@nox.session(tags=["format", "lint"])
def isort(session: nox.session) -> None:
    """Sort python imports"""
    session.install("isort")
    session.run(
        "isort",
        "--profile",
        "black",
        *format_dirs,
    )

    skiyfile = "src/skiylia.py"

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

    args = parse_args(session)
    buildnum = fetch_build_number(session) + int(args.newcommit)

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

    # Skiylia versioning
    from skiylia import Skiylia

    # fetch the build arguments
    args = parse_args(session)

    session.debug("Checking skiylia versioning information")
    buildnum = fetch_build_number(session) + int(args.newcommit)

    last_ver = args.last_ver if args.last_ver else fetch_last_release(session)
    session.debug(f"Last version {last_ver} {'given' if args.last_ver else 'found'}")

    # incorrect build number
    if Skiylia.Version.build != buildnum:
        session.error(f"{Skiylia.name} build incorrect (should be '{buildnum}')")
    # incorrect identifier label
    if Skiylia.Version.ident and Skiylia.Version.ident not in [
        "pre-alpha",
        "alpha",
        "beta",
    ]:
        session.error(
            f"{Skiylia.name} stage incorrect, {Skiylia.Version.ident} invalid"
        )
    # version number not larger than latest release
    last_ver_tuple = tuple(int(x) for x in last_ver.split("."))
    this_ver_tuple = (
        Skiylia.Version.major,
        Skiylia.Version.minor,
        Skiylia.Version.patch,
    )
    if last_ver_tuple > this_ver_tuple:
        session.error(
            f"{Skiylia.name} version incorrect: should be larger than {last_ver}"
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

    # fetch the build arguments
    args = parse_args(session)

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
        "-vv" if args.debug else "-v",
    )
    session.run("coverage", "report", "-m")


@nox.session
def skiytests(session: nox.session) -> None:
    """Run the skiylia test suite (Non-functional for now)"""
    # session.run("python3 src/skiylia.py")


@nox.session()
def changelog(session: nox.session) -> None:
    """Generate (or update) the changelog from commit history.
    use -- force-regen to force the changelog to update."""

    def commits_since_last(session: nox.session, last: str) -> list[str]:
        bots = ["Mergify"]
        sep = "\2"
        commits = session.run(
            "git",
            "log",
            f"v{last}..HEAD",
            "--no-merges",
            f"--pretty='%h{sep}%cn{sep}%s'",
            "--abbrev-commit",
            # "--oneline",
            silent=True,
            external=True,
        ).split("\n")[:-1]
        return [
            commit[1:-1].split(sep)
            for commit in commits
            for bot in bots
            if bot not in commit
        ]

    def commits_to_log_entry(commits: list[str, str, str]) -> dict[str, list[str]]:
        headings, log = {
            "fix": "Fixes",
            "chg": "Improvements",
            "new": "New features",
        }, {}
        for _, author, commit in commits:
            tpe = re.search(rf"({'|'.join(headings.keys())}):", commit)
            if tpe:
                small_head = tpe.group()[:-1]
                head = headings[small_head]
                log[head] = log.get(head, []) + [commit[len(small_head) + 1 :]]
                log["Contributors"] = log.get("Contributors", set()).union({author})
        return "\n\n".join(
            [
                f"### {header}\n"
                + "\n".join(
                    [
                        f" - {text.strip().capitalize()}.".replace("..", ".")
                        for text in entries
                    ]
                )
                for header, entries in sorted(log.items())
            ]
        )

    def to_rst(clog: str) -> str:
        to_replace = [line for line in clog.split("\n") if re.search(r"^#{1,3} ", line)]
        for replace in to_replace:
            heading_level = re.search(r"^#{1,3} ", replace).group()
            underline = ["=", "-", "~"][heading_level.count("#") - 1]
            year = re.search(r"\([0-9]{4}\-[0-9]{2}\-[0-9]{2}\)", replace)
            title = (
                replace[len(heading_level) :]
                if not year
                else replace[len(heading_level) : -len(year.group())]
            )
            clog = clog.replace(
                replace,
                replace.replace(heading_level, "")
                .replace(year.group(), "")
                .replace(
                    title,
                    f"{title}\n"
                    + underline * len(title)
                    + f"\n:Date: {year.group()[1:-1]}",
                )
                if year
                else replace.replace(heading_level, "").replace(
                    title, f"{title}\n" + underline * len(title)
                ),
            )
        return clog

    import time

    from skiylia import Skiylia

    change_log_file = "CHANGELOG.md"
    change_log_rst = "docs/source/changelog.rst"

    # arguments passed to the function
    force = session.posargs and session.posargs == ["force-regen"]
    if session.posargs and session.posargs == ["delete"]:
        if os.path.exists(change_log_file):
            os.remove(change_log_file)
        if os.path.exists(change_log_rst):
            os.remove(change_log_rst)
        session.skip("Deleted changelog")

    # fetch the old skiylia version
    last_ver = fetch_last_release(session)
    session.log(f"Fetching changes since {last_ver}")

    # fetch the current skiylia version
    V = Skiylia.Version
    this_ver = ".".join(str(x) for x in [V.major, V.minor, V.patch]) + (
        f" [{V.ident}]" if V.ident else ""
    )
    version_title = f"{this_ver} ({time.strftime('%Y-%m-%d', time.gmtime())})"

    # fetch the commits as a changelog entry
    commits = commits_since_last(session, last_ver)
    log_entry = commits_to_log_entry(commits)
    if not log_entry and not force:
        session.skip("No commits to add this version!")
    new_entry = "\n\n".join(
        [
            f"## {version_title}",
            log_entry,
        ]
    )
    session.log(f"{len(commits)} commits for {this_ver}")

    # fetch the current changelog
    title = "# Changes"
    clog = title
    if os.path.exists(change_log_file):
        with open(change_log_file, "r") as f:
            clog = f.read()

    # fetch a list of all changelog versions
    vernum = r"\d+\.\d+\.\d+"
    idents = r"(?: | \[\b(?:pre\-alpha|alpha|beta)\b\] )"
    isoyear = r"\([0-9]{4}\-[0-9]{2}\-[0-9]{2}\)"
    versions = re.findall(rf"{vernum}{idents}{isoyear}", clog)
    version_idxs = [clog.find(version) for version in versions] + [len(clog)]

    # fetch the logs for each version
    version_logs = dict(
        [
            (
                version.replace(re.search(isoyear, version).group(), "").strip(),
                "## " + clog[version_idxs[i] : version_idxs[i + 1] - 2],
            )
            for i, version in enumerate(versions)
        ]
    )

    # check if this version already has a section
    has_this_ver = [this_ver in v for v in versions]
    if any(has_this_ver):
        changed = version_logs[this_ver] != new_entry
        version_logs[this_ver] = new_entry
        if changed:
            session.log(f"Updating changelog section {this_ver}")
    # otherwise, add to the start of the changelog
    else:
        changed = True
        session.log("Adding new changelog section")
        version_logs = {this_ver: new_entry} | version_logs

    # Update the changelog if it has been changed
    if changed or force:
        session.log("Writing to changelog")
        clog = "\n\n".join([title] + list(version_logs.values()) + [""])
        rst_log = to_rst(clog)
        with open(change_log_file, "w") as f:
            f.write(clog)
        with open(change_log_rst, "w") as f:
            f.write(rst_log)
    else:
        session.log("Changelog did not require updating")
