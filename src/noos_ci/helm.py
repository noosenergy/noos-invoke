import os

from invoke import task

from . import utils


CHARTMUSEUM_REPO = "noos-private"
CHARTMUSEUM_URL = "https://charts.noos.energy"
CHARTMUSEUM_TOKEN = os.getenv("CHARTMUSEUM_TOKEN")
CHARTMUSEUM_PLUGINS = ["https://github.com/chartmuseum/helm-push.git"]


# Helm deployment workflow:


@task
def login(
    ctx, repo=CHARTMUSEUM_REPO, url=CHARTMUSEUM_URL, user="noosenergy", token=CHARTMUSEUM_TOKEN
):
    """Login to Helm remote registry (Chart Museum)."""
    assert token is not None, "Missing remote Helm registry token."
    ctx.run(f"helm repo add {repo} {url} --username {user} --password {token}", pty=True)


@task
def install(ctx, plugins=CHARTMUSEUM_PLUGINS):
    """Provision local Helm client (Chart Museum Plugin)."""
    for plugin in plugins:
        ctx.run(f"helm plugin install {plugin}", pty=True)


@task
def lint(ctx, chart="./helm/chart"):
    """Check compliance of Helm charts / values."""
    utils.check_path(chart)
    ctx.run(f"helm lint {chart}", pty=True)


@task(help={"dry-run": "Whether to render the Helm manifest first"})
def test(
    ctx,
    chart="./helm/chart",
    values="./local/helm-values.yaml",
    release="test",
    namespace="default",
    context="minikube",
    dry_run=False,
):
    """Test local deployment in Minikube."""
    utils.check_path(chart)
    utils.check_path(values)
    cmd = f"helm install {release} {chart} --values {values} "
    cmd += f"--create-namespace --namespace {namespace} --context {context} "
    if dry_run:
        cmd += "--dry-run --debug"
    ctx.run(cmd, pty=True)


@task
def push(ctx, chart="./helm/chart", repo=CHARTMUSEUM_REPO):
    """Push Helm chart to a remote registry."""
    utils.check_path(chart)
    ctx.run(f"helm push {chart} {repo}", pty=True)
