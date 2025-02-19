from invoke import Context, task


CONFIG = {
    "git": {
        "token": None,
    }
}


@task()
def config(ctx: Context, token: str | None = None) -> None:
    """Setup git credentials with a Github token."""
    token = token or ctx.git.token
    assert token is not None, "Missing Github tokem."
    ctx.run("git config --global --unset url.ssh://git@github.com.insteadof")
    ctx.run(f"echo https://{token}:@github.com > ~/.git-credentials")
    ctx.run("git config --global credential.helper store")
