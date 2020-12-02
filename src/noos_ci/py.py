import os

from invoke import task

from . import utils


PYPI_TOKEN = os.getenv("PYPI_TOKEN")


# Python deployment workflow


@task
def clean(ctx):
    """Clean project from temp files / dirs."""
    ctx.run("rm -rf build dist", pty=True)
    ctx.run("find src -type d -name __pycache__ | xargs rm -rf", pty=True)


@task
def format(ctx, target="./src"):
    """Auto-format source code."""
    utils.check_path(target)
    ctx.run(f"black {target}", pty=True)
    ctx.run(f"isort {target}", pty=True)


@task
def lint(ctx, target="./src"):
    """Run python linters."""
    utils.check_path(target)
    ctx.run(f"black --check {target}", pty=True)
    ctx.run(f"isort --check-only {target}", pty=True)
    ctx.run(f"pydocstyle {target}", pty=True)
    ctx.run(f"flake8 {target}", pty=True)
    ctx.run(f"mypy {target}", pty=True)


@task
def test(ctx, target="./src/tests", group=None):
    """Run pytest with optional grouped tests."""
    path = target
    if group:
        path += "/" + group
    utils.check_path(path)
    ctx.run(f"pytest {target}", pty=True)


@task
def package(ctx, target="./src/tests", group=None):
    """Build project wheel distribution."""
    ctx.run("poetry build", pty=True)


@task
def release(ctx, user="noosenergy", token=PYPI_TOKEN, group=None):
    """Publish wheel distribution to PyPi."""
    assert token is not None, "Missing remote PyPi registry token."
    ctx.run(f"poetry publish --build -u {user} -p {token}", pty=True)
