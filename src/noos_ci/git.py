import os

from invoke import Collection, task


CONFIG = {
    "git": {
        "token": os.getenv("GITHUB_TOKEN"),
    }
}


@task
def config(ctx, token=None):
    """Setup git credentials with a Github token."""
    token = token or ctx.git.token
    assert token is not None, "Missing Github tokem."
    ctx.run("git config --global --unset url.ssh://git@github.com.insteadof", pty=True)
    ctx.run(f"echo https://{token}:@github.com > ~/.git-credentials", pty=True)
    ctx.run("git config --global credential.helper store", pty=True)


ns = Collection("git")
ns.configure(CONFIG)
ns.add_task(config)
