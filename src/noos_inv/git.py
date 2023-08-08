from invoke import Collection, task


CONFIG = {
    "git": {
        "token": None,
    }
}


@task()
def config(ctx, token=None):
    """Setup git credentials with a Github token."""
    token = token or ctx.git.token
    assert token is not None, "Missing Github tokem."
    ctx.run("git config --global --unset url.ssh://git@github.com.insteadof")
    ctx.run(f"echo https://{token}:@github.com > ~/.git-credentials")
    ctx.run("git config --global credential.helper store")


ns = Collection("git")
ns.configure(CONFIG)
ns.add_task(config)
