import json
import logging
import pathlib

from invoke import Collection, Context, task

from . import utils


logger = logging.getLogger(__name__)


CONFIG = {
    "local": {
        # Sensitive
        "config": None
    }
}


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


@task(
    help={
        "service": "Forward port only for this configured service",
        "unforward": "Unforward ports without forwarding them again",
        "config": "Configuration file defining pods to port-forward",
    }
)
def ports(
    ctx: Context,
    service: str = "all",
    unforward: bool = False,
    config: str | None = None,
) -> None:
    """Forward ports for defined Kubernetes pods."""
    config = config or ctx.local.config
    assert config is not None, "Missing forward ports config file."
    # Load config file
    utils.check_path(config)
    with pathlib.Path(config).open(mode="rt") as f:
        local_config: utils.ServicesConfig = json.load(f).get("services")
    utils.check_schema(local_config)
    # Narrow-down config if necessary
    tmp_config: utils.ServicesConfig
    if service == "all":
        tmp_config = local_config
    else:
        assert service is not local_config, "Missing service in config file."
        tmp_config = {service: local_config[service]}
    # Iterate over targeted services
    filtered_pods = _filter_pods(ctx, tmp_config)
    for service, pod_config in tmp_config.items():
        if unforward:
            # Unforward port
            _unforward(ctx, pod_config)
        else:
            # Forward port
            _forward(ctx, pod_config, filtered_pods[service])


def _filter_pods(ctx: Context, config: utils.ServicesConfig) -> dict[str, str]:
    """Filter all matching pods in a given namespace."""
    # Query all pods in the namespace
    cmd_tpl = "kubectl get pod -n {namespace} "
    # Select only the name
    cmd_tpl += "-o=custom-columns=NAME:.metadata.name "
    # Filter out pods with the prefix
    cmd_tpl += " | grep {prefix}"
    # Build data struct {service: pod_name}
    selected_pods: dict[str, str] = {}
    for service, pod_config in config.items():
        cmd = cmd_tpl.format(
            namespace=pod_config["pod_namespace"],
            prefix=pod_config["pod_prefix"],
        )
        result = ctx.run(cmd, hide=True)
        if result is None:
            logger.error(f"Failed to fetch pods for {service}. Skip!")
            continue
        selected_pods[service] = result.stdout.rstrip()
    # Return selected pod names for each service
    return selected_pods


def _get_kubectl_command(namespace: str, name: str, port: int, local_port: int) -> str:
    """Get the command to forward a port to a pod."""
    return f"kubectl port-forward -n {namespace} {name} {local_port}:{port}"


def _forward(ctx: Context, config: utils.PodConfig, pod_name: str) -> None:
    """Forward port matching configuration."""
    # Build kubectl port-forward command
    cmd = _get_kubectl_command(
        config["pod_namespace"],
        pod_name,
        config["pod_port"],
        config["local_port"],
    )
    # Ensure the process is detached
    cmd += " </dev/null >/dev/null 2>&1 &"
    logger.info(f"Forwarding {pod_name} to {config['local_port']}")
    ctx.run(cmd, warn=True, hide=True)


def _unforward(ctx: Context, config: utils.PodConfig) -> None:
    """Unforward port matching configuration."""
    # Build kubectl port-forward command
    cmd = _get_kubectl_command(
        config["pod_namespace"],
        config["pod_prefix"] + ".*",
        config["pod_port"],
        config["local_port"],
    )
    # Fetch running processes
    cmd = f"ps aux | grep '{cmd}' | grep -v grep"
    # Restrict to only pid part
    cmd += " | awk '{print $2}'"
    result = ctx.run(cmd, hide=True)
    # Kill the process
    if result is not None:
        logger.info(f"Killing previous port-forward for {config['pod_prefix']}")
        ctx.run(f"kill -9 {result.stdout.rstrip()}", warn=True, hide=True)


ns = Collection("local")
ns.configure(CONFIG)
ns.add_task(dotenv)
ns.add_task(ports)
