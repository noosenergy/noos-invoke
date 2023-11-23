import os
from typing import Optional

from invoke import Collection, Context, task

from . import utils


CONFIG = {
    "docker": {
        # Sensitive
        "repo": None,
        "user": "AWS",
        "token": None,
        "arg": None,
        # Non-sensitive
        "name": "webserver",
        "context": ".",
        "file": "Dockerfile",
        "tag": "test",
        "platform": "linux/arm64,linux/amd64",
    }
}


# Docker deployment workflow:


@task()
def login(ctx, repo=None, user=None, token=None):
    """Login to Docker remote registry (AWS ECR or Dockerhub)."""
    user = user or ctx.docker.user
    if user == utils.UserType.AWS:
        _aws_login(ctx, repo)
    else:
        _dockerhub_login(ctx, user, token)


def _aws_login(ctx: Context, repo: Optional[str]) -> None:
    repo = repo or ctx.docker.repo
    assert repo is not None, "Missing remote AWS ECR URL."
    cmd = "aws ecr get-login-password | "
    cmd += f"docker login --username AWS --password-stdin {repo}"
    ctx.run(cmd)


def _dockerhub_login(ctx: Context, user: str, token: Optional[str]) -> None:
    token = token or ctx.docker.token
    assert token is not None, "Missing remote Dockerhub token."
    ctx.run(f"docker login --username {user} --password {token}")


@task()
def build(ctx, name=None, context=None, file=None, arg=None):
    """Build Docker image locally."""
    name = name or ctx.docker.name
    context = context or ctx.docker.context
    utils.check_path(context)
    file = file or f"{context}/{ctx.docker.file}"
    utils.check_path(file)
    arg = arg or ctx.docker.arg
    cmd = f"docker build --pull --file {file} --tag {name} "
    if arg is not None:
        assert arg in os.environ, f"Missing environment variable {arg}."
        cmd += f"--build-arg {arg}={os.environ[arg]} "
    cmd += f"{context}"
    ctx.run(cmd)


@task(
    help={
        "tag-only": "Whether to not tag the Docker image as latest",
        "dry-run": "Whether to only tag the Docker image and to not push",
    }
)
def push(ctx, repo=None, name=None, tag=None, tag_only=False, dry_run=False):
    """Push Docker image to a remote registry."""
    repo = repo or ctx.docker.repo
    name = name or ctx.docker.name
    tag = tag or ctx.docker.tag
    tag_list = [tag] if tag_only else [tag, "latest"]
    for t in tag_list:
        target_name = f"{repo}/{name}:{t}"
        ctx.run(f"docker tag {name} {target_name}")
        if not dry_run:
            ctx.run(f"docker push {target_name}")


@task(help={"tag-only": "Whether to not tag the Docker image as latest"})
def buildx(
    ctx,
    repo=None,
    name=None,
    context=None,
    file=None,
    arg=None,
    platform=None,
    tag=None,
    tag_only=False,
):
    """Build and push x-platform Docker image to a remote registry.

    :Warning:
    Without using `--push` option to push the image, expect the error:

    ```No output specified with docker-container driver.
    Build result will only remain in the build cache.```

    To push image into registry use `--push`
    or to load image into docker use `--load`

    In addition: `--load` option does not work for multiple platforms
    """
    repo = repo or ctx.docker.repo
    name = name or ctx.docker.name
    context = context or ctx.docker.context
    utils.check_path(context)
    file = file or f"{context}/{ctx.docker.file}"
    utils.check_path(file)
    arg = arg or ctx.docker.arg
    platform = platform or ctx.docker.platform
    tag = tag or ctx.docker.tag
    tag_list = [tag] if tag_only else [tag, "latest"]
    for t in tag_list:
        target_name = f"{repo}/{name}:{t}"
        cmd = f"docker buildx build --pull --file {file} --tag {target_name} "
        if arg is not None:
            assert arg in os.environ, f"Missing environment variable {arg}."
            cmd += f"--build-arg {arg}={os.environ[arg]} "
        cmd += f"--platform {platform} --push {context}"
        ctx.run(cmd)


ns = Collection("docker")
ns.configure(CONFIG)
ns.add_task(login)
ns.add_task(build)
ns.add_task(buildx)
ns.add_task(push)
