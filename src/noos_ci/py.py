import os

from invoke import Collection, task

from . import utils


CONFIG = {
    "py": {
        "target": "./src",
        "user": "__token__",
        "token": os.getenv("PYPI_TOKEN"),
    }
}


# Python deployment workflow


@task
def clean(ctx):
    """Clean project from temp files / dirs."""
    ctx.run("rm -rf build dist", pty=True)
    ctx.run("find src -type d -name __pycache__ | xargs rm -rf", pty=True)


@task
def format(ctx, target=None):
    """Auto-format source code."""
    target = target or ctx.py.target
    utils.check_path(target)
    ctx.run(f"black {target}", pty=True)
    ctx.run(f"isort {target}", pty=True)


@task
def lint(ctx, target=None):
    """Run python linters."""
    target = target or ctx.py.target
    utils.check_path(target)
    ctx.run(f"black --check {target}", pty=True)
    ctx.run(f"isort --check-only {target}", pty=True)
    ctx.run(f"pydocstyle {target}", pty=True)
    ctx.run(f"flake8 {target}", pty=True)
    ctx.run(f"mypy {target}", pty=True)


@task
def test(ctx, target=None, group=None):
    """Run pytest with optional grouped tests."""
    path = target or ctx.py.target
    if group:
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
