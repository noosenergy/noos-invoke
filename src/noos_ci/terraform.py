import terraform_client
from invoke import Collection, task


CONFIG = {
    "terraform": {
        "organisation": None,
        "workspace": None,
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
    terraform_client.update_workspace_variable(organisation, workspace, token, variable, value)
    print(f"Updated Terraform {variable!r} value to {value!r}")


@task
def plan(ctx, message="", organisation=None, workspace=None, token=None):
    """Run a plan in Terraform cloud."""
    organisation = organisation or ctx.terraform.organisation
    workspace = workspace or ctx.terraform.workspace
    token = token or ctx.terraform.token
    url = terraform_client.create_workspace_run(organisation, workspace, token, message)
    print(f"Running Terraform plan for {workspace}: {url}")


ns = Collection("terraform")
ns.configure(CONFIG)
ns.add_task(update)
ns.add_task(plan)
