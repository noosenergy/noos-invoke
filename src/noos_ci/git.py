import os

from invoke import task


GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")


@task
def config(ctx, token=GITHUB_TOKEN):
    """Setup git credentials with a Github token."""
    ctx.run("git config --global --unset url.ssh://git@github.com.insteadof", pty=True)
    ctx.run(f"echo https://{token}:@github.com > ~/.git-credentials", pty=True)
    ctx.run("git config --global credential.helper store", pty=True)
