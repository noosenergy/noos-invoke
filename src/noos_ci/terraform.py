from invoke import Collection, task


CONFIG = {
    "terraform": {
        "organisation": "noosenergy",
        "workspace": "noos-prod",
        "token": None,
    }
}


# Terraform deployment workflow


@task
def update(ctx, variable="", value="", organisation=None, workspace=None, token=None):
    """Update variable in Terraform cloud."""
    organisation = organisation or ctx.terraform.organisation
    workspace = workspace or ctx.terraform.workspace
    token = token or ctx.terraform.token
    assert token is not None, "Missing Terraform Cloud token."
    cmd = f"noostf update --variable {variable} --value '{value}' "
    cmd += f"--organisation {organisation} --workspace {workspace} --token {token}"
    ctx.run(cmd, pty=True)


@task
def run(ctx, message="", organisation=None, workspace=None, token=None):
    """Run a plan in Terraform cloud."""
    organisation = organisation or ctx.terraform.organisation
    workspace = workspace or ctx.terraform.workspace
    token = token or ctx.terraform.token
    assert token is not None, "Missing Terraform Cloud token."
    cmd = f"noostf run --message '{message}' "
    cmd += f"--organisation {organisation} --workspace {workspace} --token {token}"
    breakpoint()
    ctx.run(cmd, pty=True)


ns = Collection("terraform")
ns.configure(CONFIG)
ns.add_task(update)
ns.add_task(run)
