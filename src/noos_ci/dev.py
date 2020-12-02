from invoke import task

from . import utils


# Local development workflow


@task(help={"force": "Whether to destroy the existing file first"})
def dotenv(ctx, template="./dotenv.tpl", target="./.env", force=False):
    """Create local dotenv file."""
    utils.check_path(template)
    try:
        utils.check_path(target)
        if force:
            raise utils.PathNotFound
    except utils.PathNotFound:
        ctx.run(f"cp {template} {target}", pty=True)
