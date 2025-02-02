from enum import Enum, StrEnum, auto

from invoke import Collection, Context, task

from . import utils


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


class InstallType(str, Enum):
    poetry = "poetry"
    pipenv = "pipenv"
    uv = "uv"

    @classmethod
    def get(cls, ctx: Context, value: str | None) -> str:
        install = value or ctx.python.install
        assert install in cls.__members__, f"Unknown Python installation {install}."
        return install


class GroupType(StrEnum):
    unit = auto()
    integration = auto()
    functional = auto()


class FormatterType(StrEnum):
    BLACK = auto()
    ISORT = auto()
    RUFF = auto()


class LinterType(StrEnum):
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
    source: str | None = None,
    install: str | None = None,
    formatters: str | None = None,
) -> None:
    """Auto-format source code."""
    source = source or ctx.python.source
    utils.check_path(source)
    cmd = _activate_shell(ctx, install)
    list_formatters = formatters.split(",") if formatters else ctx.python.formatters.split(",")
    for formatter in list_formatters:
        match formatter:
            case FormatterType.BLACK:
                ctx.run(cmd + f"black {source}", pty=True)
            case FormatterType.ISORT:
                ctx.run(cmd + f"isort {source}", pty=True)
            case FormatterType.RUFF:
                ctx.run(cmd + f"ruff check --select I --fix {source}", pty=True)
                ctx.run(cmd + f"ruff format {source}", pty=True)
            case _:
                raise ValueError(f"Unexpected formatter {formatter}")


@task()
def lint(
    ctx: Context, source: str | None = None, install: str | None = None, linters: str | None = None
) -> None:
    """Run python linters."""
    source = source or ctx.python.source
    utils.check_path(source)
    cmd = _activate_shell(ctx, install)
    list_linters = linters.split(",") if linters else ctx.python.linters.split(",")
    for linter in list_linters:
        match linter:
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
                ctx.run(cmd + f"ruff check {source}", pty=True)
            case LinterType.IMPORTS:
                ctx.run(cmd + "lint-imports", pty=True)
            case _:
                raise ValueError(f"Unexpected linter {linter}")


@task()
def test(
    ctx: Context, tests: str | None = None, group: str = "", install: str | None = None
) -> None:
    """Run pytest with optional grouped tests."""
    tests = tests or ctx.python.tests
    if group != "":
        assert group in GroupType.__members__, f"Unknown py.test group {group}."
        tests += "/" + group
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
    install_type = InstallType.get(ctx, install)
    if install_type == InstallType.poetry:
        ctx.run("poetry build", pty=True)
    if install_type == InstallType.pipenv:
        ctx.run("pipenv run python -m build -n", pty=True)
    if install_type == InstallType.uv:
        ctx.run("uvx --from build pyproject-build --installer uv")


@task()
def release(
    ctx: Context, user: str | None = None, token: str | None = None, install: str | None = None
) -> None:
    """Publish wheel distribution to PyPi."""
    user = user or ctx.python.user
    token = token or ctx.python.token
    assert user is not None, "Missing remote PyPi registry user."
    assert token is not None, "Missing remote PyPi registry token."
    install_type = InstallType.get(ctx, install)
    if install_type == InstallType.poetry:
        ctx.run(f"poetry publish --build -u {user} -p {token}", pty=True)
    if install_type == InstallType.pipenv:
        raise NotImplementedError
    if install_type == InstallType.uv:
        ctx.run(f"uvx twine upload dist/* -u {user} -p {token}")


def _activate_shell(ctx: Context, install: str | None) -> str:
    install_type = InstallType.get(ctx, install)
    return f"{install_type} run "


ns = Collection("python")
ns.configure(CONFIG)
ns.add_task(clean)
ns.add_task(format)
ns.add_task(lint)
ns.add_task(test)
ns.add_task(coverage)
ns.add_task(package)
ns.add_task(release)
