import enum

from invoke import Collection, task

from . import utils


CONFIG = {
    "python": {
        "install": "pipenv",
        "source": "./src",
        "tests": "./src/tests",
        "user": "__token__",
        "token": None,
    }
}


class InstallType(str, enum.Enum):
    poetry = "poetry"
    pipenv = "pipenv"

    @classmethod
    def get(cls, ctx, value):
        install = value or ctx.python.install
        assert install in cls.__members__, f"Unknown Python installation {install}."
        return install


class GroupType(str, enum.Enum):
    unit = "unit"
    integration = "integration"
    functional = "functional"


# Python deployment workflow


@task
def clean(ctx):
    """Clean project from temp files / dirs."""
    ctx.run("rm -rf build dist", pty=True)
    ctx.run("find src -type d -name __pycache__ | xargs rm -rf", pty=True)


@task
def format(ctx, source=None, install=None):
    """Auto-format source code."""
    source = source or ctx.python.source
    utils.check_path(source)
    cmd = f"{InstallType.get(ctx, install)} run "
    ctx.run(cmd + f"black {source}", pty=True)
    ctx.run(cmd + f"isort {source}", pty=True)


@task
def lint(ctx, source=None, install=None):
    """Run python linters."""
    source = source or ctx.python.source
    utils.check_path(source)
    cmd = f"{InstallType.get(ctx, install)} run "
    ctx.run(cmd + f"black --check {source}", pty=True)
    ctx.run(cmd + f"isort --check-only {source}", pty=True)
    ctx.run(cmd + f"pydocstyle {source}", pty=True)
    ctx.run(cmd + f"flake8 {source}", pty=True)
    ctx.run(cmd + f"mypy {source}", pty=True)


@task
def test(ctx, tests=None, group=None, install=None):
    """Run pytest with optional grouped tests."""
    path = tests or ctx.python.tests
    if group:
        assert group in GroupType.__members__, f"Unknown py.test group {group}."
        path += "/" + group
    utils.check_path(path)
    cmd = f"{InstallType.get(ctx, install)} run "
    ctx.run(cmd + f"pytest {path}", pty=True)


@task
def package(ctx, install=None):
    """Build project wheel distribution."""
    install = InstallType.get(ctx, install)
    if install == InstallType.poetry:
        ctx.run("poetry build", pty=True)
    if install == InstallType.pipenv:
        ctx.run("pipenv run python setup.py sdist", pty=True)


@task
def release(ctx, user=None, token=None, install=None):
    """Publish wheel distribution to PyPi."""
    user = user or ctx.python.user
    token = token or ctx.python.token
    assert token is not None, "Missing remote PyPi registry token."
    install = InstallType.get(ctx, install)
    if install == InstallType.poetry:
        ctx.run(f"poetry publish --build -u {user} -p {token}", pty=True)
    if install == InstallType.pipenv:
        raise NotImplementedError


ns = Collection("python")
ns.configure(CONFIG)
ns.add_task(clean)
ns.add_task(format)
ns.add_task(lint)
ns.add_task(test)
ns.add_task(package)
ns.add_task(release)
