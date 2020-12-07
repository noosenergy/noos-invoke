import enum

from invoke import Collection, task

from . import utils


CONFIG = {
    "py": {
        "source": "./src",
        "tests": "./src/tests",
        "user": "__token__",
        "token": None,
    }
}


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
def format(ctx, source=None):
    """Auto-format source code."""
    source = source or ctx.py.source
    utils.check_path(source)
    ctx.run(f"black {source}", pty=True)
    ctx.run(f"isort {source}", pty=True)


@task
def lint(ctx, source=None):
    """Run python linters."""
    source = source or ctx.py.source
    utils.check_path(source)
    ctx.run(f"black --check {source}", pty=True)
    ctx.run(f"isort --check-only {source}", pty=True)
    ctx.run(f"pydocstyle {source}", pty=True)
    ctx.run(f"flake8 {source}", pty=True)
    ctx.run(f"mypy {source}", pty=True)


@task
def test(ctx, tests=None, group=None):
    """Run pytest with optional grouped tests."""
    path = tests or ctx.py.tests
    if group:
        assert group in GroupType.__members__, f"Unknown py.test group {group}."
        path += "/" + group
    utils.check_path(path)
    ctx.run(f"pytest {path}", pty=True)


@task
def package(ctx):
    """Build project wheel distribution."""
    ctx.run("poetry build", pty=True)


@task
def release(ctx, user=None, token=None):
    """Publish wheel distribution to PyPi."""
    user = user or ctx.py.user
    token = token or ctx.py.token
    assert token is not None, "Missing remote PyPi registry token."
    ctx.run(f"poetry publish --build -u {user} -p {token}", pty=True)


ns = Collection("py")
ns.configure(CONFIG)
ns.add_task(clean)
ns.add_task(format)
ns.add_task(lint)
ns.add_task(test)
ns.add_task(package)
ns.add_task(release)
