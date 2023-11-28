from invoke import Collection, Context, task

from . import utils


# Local development workflow


@task(help={"force": "Whether to destroy the existing file first"})
def dotenv(
    ctx: Context,
    template: str = "./dotenv.tpl",
    target: str = "./.env",
    force: bool = False,
) -> None:
    """Create local dotenv file."""
    utils.check_path(template)
    try:
        utils.check_path(target)
        if force:
            raise utils.PathNotFound
    except utils.PathNotFound:
        ctx.run(f"cp {template} {target}")


ns = Collection("local")
ns.add_task(dotenv)
