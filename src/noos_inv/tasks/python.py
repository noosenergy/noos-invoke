from enum import StrEnum, auto

from invoke import Context, task

from noos_inv import utils


CONFIG = {
    "python": {
        "install": "pipenv",
        "source": "./src",
        "formatters": "ruff",
        "linters": "ruff,mypy",
        "tests": "./src/tests",
        "user": None,
        "token": None,
    }
}


class ValidatedEnum(StrEnum):
    @classmethod
    def get(cls, value: str) -> StrEnum:
        assert value in cls, f"Unknown {cls.__name__} {value}."
        return cls(value)


class InstallType(ValidatedEnum):
    PIPENV = auto()
    POETRY = auto()
    UV = auto()


class GroupType(ValidatedEnum):
    UNIT = auto()
    INTEGRATION = auto()
    FUNCTIONAL = auto()


class FormatterType(ValidatedEnum):
    BLACK = auto()
    ISORT = auto()
    RUFF = auto()


class LinterType(ValidatedEnum):
    BLACK = auto()
    ISORT = auto()
    PYDOCSTYLE = auto()
    FLAKE8 = auto()
    RUFF = auto()
    MYPY = auto()
    IMPORTS = auto()


# Python deployment workflow


@task()
def clean(ctx: Context) -> None:
    """Clean project from temp files / dirs."""
    ctx.run("rm -rf build dist")
    ctx.run("find src -type d -name __pycache__ | xargs rm -rf")


@task()
def format(
    ctx: Context,
    formatters: str | None = None,
    source: str | None = None,
    install: str | None = None,
) -> None:
    """Auto-format source code."""
    formatters = formatters or ctx.python.formatters
    source = source or ctx.python.source
    utils.check_path(source)
    cmd = _activate_shell(ctx, install)
    for formatter in formatters.split(","):
        match FormatterType.get(formatter):
            case FormatterType.BLACK:
                ctx.run(cmd + f"black {source}", pty=True)
            case FormatterType.ISORT:
                ctx.run(cmd + f"isort {source}", pty=True)
            case FormatterType.RUFF:
                ctx.run(cmd + f"ruff check --select I --fix {source}")
                ctx.run(cmd + f"ruff format {source}")


@task()
def lint(
    ctx: Context,
    linters: str | None = None,
    source: str | None = None,
    install: str | None = None,
) -> None:
    """Run python linters."""
    linters = linters or ctx.python.linters
    source = source or ctx.python.source
    utils.check_path(source)
    cmd = _activate_shell(ctx, install)
    for linter in linters.split(","):
        match LinterType.get(linter):
            case LinterType.BLACK:
                ctx.run(cmd + f"black --check {source}", pty=True)
            case LinterType.ISORT:
                ctx.run(cmd + f"isort --check-only {source}", pty=True)
            case LinterType.PYDOCSTYLE:
                ctx.run(cmd + f"pydocstyle {source}", pty=True)
            case LinterType.FLAKE8:
                ctx.run(cmd + f"flake8 {source}", pty=True)
            case LinterType.MYPY:
                ctx.run(cmd + f"mypy {source}", pty=True)
            case LinterType.RUFF:
                ctx.run(cmd + f"ruff check {source}")
            case LinterType.IMPORTS:
                ctx.run(cmd + "lint-imports", pty=True)


@task()
def test(
    ctx: Context, tests: str | None = None, group: str = "", install: str | None = None
) -> None:
    """Run pytest with optional grouped tests."""
    tests = tests or ctx.python.tests
    if group != "":
        tests += "/" + GroupType.get(group)
    utils.check_path(tests)
    cmd = _activate_shell(ctx, install)
    ctx.run(cmd + f"pytest {tests}", pty=True)


@task()
def coverage(
    ctx: Context,
    config: str = "setup.cfg",
    report: str = "term",
    tests: str | None = None,
    install: str | None = None,
) -> None:
    """Run coverage test report."""
    tests = tests or ctx.python.tests
    utils.check_path(tests)
    cmd = _activate_shell(ctx, install)
    ctx.run(cmd + f"pytest --cov --cov-config={config} --cov-report={report} {tests}", pty=True)


@task()
def package(ctx: Context, install: str | None = None) -> None:
    """Build project wheel distribution."""
    install = install or ctx.python.install
    match InstallType.get(install):
        case InstallType.POETRY:
            ctx.run("poetry build", pty=True)
        case InstallType.PIPENV:
            ctx.run("pipenv run python -m build -n", pty=True)
        case InstallType.UV:
            ctx.run("uvx --from build pyproject-build --installer uv")


@task()
def release(
    ctx: Context, user: str | None = None, token: str | None = None, install: str | None = None
) -> None:
    """Publish wheel distribution to PyPi."""
    user = user or ctx.python.user
    token = token or ctx.python.token
    install = install or ctx.python.install
    assert user is not None, "Missing remote PyPi registry user."
    assert token is not None, "Missing remote PyPi registry token."
    match InstallType.get(install):
        case InstallType.POETRY:
            ctx.run(f"poetry publish --build -u {user} -p {token}", pty=True)
        case InstallType.PIPENV:
            ctx.run(f"pipenv run twine upload dist/* -u {user} -p {token}", pty=True)
        case InstallType.UV:
            ctx.run(f"uvx twine upload dist/* -u {user} -p {token}")


def _activate_shell(ctx: Context, install: str | None) -> str:
    install = install or ctx.python.install
    return f"{InstallType.get(install)} run "
