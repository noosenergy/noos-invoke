import os

from invoke import Collection, task

from . import utils


CONFIG = {
    "docker": {
        "repo": os.getenv("AWS_ECR_URL", "noosenergy"),
        "user": "noosenergy",
        "token": os.getenv("DOCKERHUB_TOKEN"),
        "name": "noos-prod",
        "context": ".",
        "tag": "test",
    }
}


# Docker deployment workflow:


@task
def login(ctx, repo=None, user=None, token=None):
    """Login to Docker remote registry (AWS ECR or Dockerhub)."""
    user = user or ctx.docker.user
    if user == "AWS":
        _aws_login(ctx, repo)
    _dockerhub_login(ctx, user, token)


def _aws_login(ctx, repo):
    repo = repo or ctx.docker.repo
    assert repo is not None, "Missing remote AWS ECR URL."
    cmd = "aws ecr get-login-password | "
    cmd += f"docker login --username AWS --password-stdin {repo}"
    ctx.run(cmd, pty=True)


def _dockerhub_login(ctx, user, token):
    token = token or ctx.docker.token
    assert token is not None, "Missing remote Dockerhub token."
    ctx.run(f"docker login --username {user} --password {token}", pty=True)


@task
def build(ctx, name=None, context=None):
    """Build Docker image locally."""
    name = name or ctx.docker.name
    context = context or ctx.docker.context
    utils.check_path(context)
    cmd = f"docker build --pull --tag {name} "
    if "GITHUB_TOKEN" in os.environ:
        cmd += f"--build-arg GITHUB_TOKEN={os.environ['GITHUB_TOKEN']} "
    cmd += f"{context}"
    ctx.run(cmd, pty=True)


@task(help={"dry-run": "Whether to tag the Docker image only"})
def push(ctx, repo=None, name=None, tag=None, dry_run=False):
    """Push Docker image to a remote registry."""
    repo = repo or ctx.docker.repo
    name = name or ctx.docker.name
    tag = tag or ctx.docker.tag
    for t in [tag, "latest"]:
        target_name = f"{repo}/{name}:{t}"
        ctx.run(f"docker tag {name} {target_name}", pty=True)
        if not dry_run:
            ctx.run(f"docker push {target_name}", pty=True)


ns = Collection("docker")
ns.configure(CONFIG)
ns.add_task(login)
ns.add_task(build)
ns.add_task(push)
