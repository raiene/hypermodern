"""Nox sessions."""

import nox
from nox.sessions import Session


package = "hypermodern"
nox.options.sessions = "lint", "mypy", "tests"
locations = "src", "tests", "noxfile.py", "docs/conf.py"


def install_all_deps(session: Session) -> None:
    """Install all dependencies using poetry."""
    session.run("poetry", "install", external=True)


@nox.session(python="3.14")
def black(session: Session) -> None:
    """Run black code formatter."""
    args = session.posargs or locations
    install_all_deps(session)
    session.run("black", *args)


@nox.session(python="3.14")
def lint(session: Session) -> None:
    """Lint using flake8."""
    args = session.posargs or locations
    install_all_deps(session)
    session.run("flake8", *args)


@nox.session(python="3.14")
def safety(session: Session) -> None:
    """Scan dependencies for insecure packages."""
    install_all_deps(session)
    session.run("safety", "check", "--project", ".", "--full-report")


@nox.session(python="3.14")
def mypy(session: Session) -> None:
    """Type-check using mypy."""
    args = session.posargs or locations
    install_all_deps(session)
    session.run("mypy", *args)


@nox.session(python="3.14")
def tests(session: Session) -> None:
    """Run the test suite."""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    install_all_deps(session)
    session.run("pytest", *args)


@nox.session(python="3.14")
def typeguard(session: Session) -> None:
    """Runtime type checking using Typeguard."""
    args = session.posargs or ["-m", "not e2e"]
    install_all_deps(session)
    session.run("pytest", f"--typeguard-packages={package}", *args)


@nox.session(python="3.14")
def xdoctest(session: Session) -> None:
    """Run examples with xdoctest."""
    args = session.posargs or ["all"]
    install_all_deps(session)
    session.run("python", "-m", "xdoctest", package, *args)


@nox.session(python="3.14")
def docs(session: Session) -> None:
    """Build the documentation."""
    install_all_deps(session)
    session.run("sphinx-build", "docs", "docs/_build")


@nox.session(python="3.14")
def coverage(session: Session) -> None:
    """Upload coverage data."""
    install_all_deps(session)
    session.run("coverage", "xml", "--fail-under=0")
    session.run("codecov", *session.posargs)
