from invoke import Collection, task

from . import utils


CONFIG = {
    "helm": {
        "repo": "local-repo",
        "url": None,
        "user": None,
        "token": None,
        "plugins": ["https://github.com/chartmuseum/helm-push.git"],
        "chart": "./helm/chart",
        "values": "./local/helm-values.yaml",
    }
}


# Helm deployment workflow:


@task
def login(ctx, repo=None, url=None, user=None, token=None):
    """Login to Helm remote registry (Chart Museum)."""
    repo = repo or ctx.helm.repo
    url = url or ctx.helm.url
    user = user or ctx.helm.user
    token = token or ctx.helm.token
    assert url is not None, "Missing remote Helm registry url."
    assert user is not None, "Missing remote Helm registry user."
    assert token is not None, "Missing remote Helm registry token."
    ctx.run(f"helm repo add {repo} {url} --username {user} --password {token}")


@task(iterable=["plugins"])
def install(ctx, plugins=None):
    """Provision local Helm client (Chart Museum Plugin)."""
    plugins = plugins or ctx.helm.plugins
    for plugin in plugins:
        ctx.run(f"helm plugin install {plugin}")


@task
def lint(ctx, chart=None):
    """Check compliance of Helm charts / values."""
    chart = chart or ctx.helm.chart
    utils.check_path(chart)
    ctx.run(f"helm lint {chart}")


@task(help={"dry-run": "Whether to render the Helm manifest first"})
def test(
    ctx,
    chart=None,
    values=None,
    release="test",
    namespace="default",
    context="minikube",
    dry_run=False,
):
    """Test local deployment in Minikube."""
    chart = chart or ctx.helm.chart
    values = values or ctx.helm.values
    utils.check_path(chart)
    utils.check_path(values)
    cmd = f"helm install {release} {chart} --values {values} "
    cmd += f"--create-namespace --namespace {namespace} --kube-context {context}"
    if dry_run:
        cmd += " --dry-run --debug"
    ctx.run(cmd)


@task
def push(ctx, chart=None, repo=None):
    """Push Helm chart to a remote registry."""
    chart = chart or ctx.helm.chart
    repo = repo or ctx.helm.repo
    utils.check_path(chart)
    ctx.run(f"helm dependency update {chart}")
    ctx.run(f"helm cm-push {chart} {repo}")


ns = Collection("helm")
ns.configure(CONFIG)
ns.add_task(login)
ns.add_task(install)
ns.add_task(lint)
ns.add_task(test)
ns.add_task(push)
