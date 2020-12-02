import os

from invoke import task

from . import utils


AWS_ECR_URL = os.getenv("AWS_ECR_URL")
DOCKERHUB_TOKEN = os.getenv("DOCKERHUB_TOKEN")
DOCKER_REPO = AWS_ECR_URL or "noosenergy"


# Docker deployment workflow:


@task
def login(ctx, url=AWS_ECR_URL, user="noosenergy", token=DOCKERHUB_TOKEN):
    """Login to Docker remote registry (AWS ECR or Dockerhub)."""
    if user == "AWS":
        _aws_login(ctx, url)
    _dockerhub_login(ctx, user, token)


def _aws_login(ctx, url):
    assert url is not None, "Missing remote AWS ECR URL."
    ctx.run(
        f"aws ecr get-login-password | docker login --username AWS --password-stdin {url}",
        pty=True,
    )


def _dockerhub_login(ctx, user, token):
    assert token is not None, "Missing remote Dockerhub token."
    ctx.run(
        f"docker login --username {user} --password {token}",
        pty=True,
    )


@task
def build(ctx, name="jupyter", context="./docker/jupyter"):
    """Build Docker image locally."""
    utils.check_path(context)
    cmd = f"docker build --pull --tag {name} "
    github_var = "GITHUB_TOKEN"
    if github_var in os.environ:
        cmd += f"--build-arg {github_var}={os.environ[github_var]} "
    cmd += f"{context}"
    ctx.run(cmd, pty=True)


@task(help={"dry-run": "Whether to tag the Docker image only"})
def push(ctx, name="jupyter", extra_tag=None, repo=DOCKER_REPO, dry_run=False):
    """Push Docker image to a remote registry."""
    target_name = f"{repo}/{name}"
    target_tags = ["latest"]
    if extra_tag:
        target_tags += extra_tag
    for tag in target_tags:
        ctx.run(f"docker tag {name} {target_name}:{tag}", pty=True)
        if not dry_run:
            ctx.run(f"docker push {target_name}:{tag}", pty=True)
