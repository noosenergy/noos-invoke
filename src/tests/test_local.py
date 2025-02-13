import json
from collections.abc import Generator

import pytest
from invoke import Config, Context

from noos_inv import local, utils


@pytest.fixture
def ctx() -> Context:
    return Context(config=Config(defaults=local.CONFIG))


@pytest.fixture
def dotenv(tmp_path) -> Generator[str, None, None]:
    tmp_file = tmp_path / "dotenv.tmpl"
    tmp_file.write_text("TEST=1")
    yield tmp_file.as_posix()


@pytest.fixture
def services_config() -> utils.ServicesConfig:
    return {
        "test1": {
            "pod_namespace": "default",
            "pod_prefix": "test1-",
            "pod_port": 80,
            "local_port": 8000,
        },
        "test2": {
            "pod_namespace": "default",
            "pod_prefix": "test2-",
            "pod_port": 80,
            "local_port": 8000,
        },
    }


@pytest.fixture
def filtered_pods(services_config) -> dict[str, str]:
    return dict(zip(services_config.keys(), services_config.keys()))


@pytest.fixture
def config(tmp_path, services_config) -> Generator[str, None, None]:
    tmp_file = tmp_path / "config.json"
    tmp_file.write_text(json.dumps({"services": services_config}))
    yield tmp_file.as_posix()


class TestDotEnv:
    def test_create_if_does_not_exist(self, test_run, ctx, dotenv):
        cmd = f"cp {dotenv} ~/new_dotenv"

        local.dotenv(ctx, template=dotenv, target="~/new_dotenv")

        test_run.assert_called_with(cmd)

    def test_not_recreate_if_exists_already(self, test_run, ctx, dotenv):
        local.dotenv(ctx, template=dotenv, target=dotenv)

        test_run.assert_not_called()

    def test_recreate_if_forced(self, test_run, ctx, dotenv):
        cmd = f"cp {dotenv} {dotenv}"

        local.dotenv(ctx, template=dotenv, target=dotenv, force=True)

        test_run.assert_called_with(cmd)


class TestPorts:
    def test_raise_error_if_missing_config(self, ctx):
        with pytest.raises(AssertionError):
            local.ports(ctx)

    def test_raise_error_if_unknown_config(self, tmp_path, ctx):
        config = tmp_path / "config.json"

        with pytest.raises(utils.PathNotFound):
            local.ports(ctx, config=config.as_posix())

    def test_raise_error_if_incorrect_config(self, tmp_path, ctx):
        config = tmp_path / "config.json"
        config.write_text('{"services": "test"}')

        with pytest.raises(utils.ValidationError):
            local.ports(ctx, config=config.as_posix())

    @pytest.mark.parametrize("unforward", [False, True])
    @pytest.mark.parametrize("service", ["all", "test1", "test2"])
    def test_execute_correct_kubectl_commands(
        self, mocker, ctx, services_config, filtered_pods, config, service, unforward
    ):
        mocked_filter = mocker.patch.object(local, "_filter_pods", return_value=filtered_pods)
        mocked_forward = mocker.patch.object(local, "_forward")
        mocked_unforward = mocker.patch.object(local, "_unforward")

        local.ports(ctx, config=config, service=service, unforward=unforward)

        mocked_filter.assert_called_once()

        if unforward:
            if service == "all":
                mocked_unforward.call_args_list == [
                    (ctx, services_config["test1"]),
                    (ctx, services_config["test2"]),
                ]
            else:
                mocked_unforward.assert_called_with(ctx, services_config[service])
        else:
            if service == "all":
                mocked_forward.call_args_list == [
                    (ctx, services_config["test1"], "test1"),
                    (ctx, services_config["test2"], "test2"),
                ]
            else:
                mocked_forward.assert_called_with(ctx, services_config[service], service)
