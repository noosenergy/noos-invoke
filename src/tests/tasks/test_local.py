import json
from collections.abc import Generator

import pytest
from invoke import Config, Context

from noos_inv import exceptions, types
from noos_inv.tasks import local


@pytest.fixture
def ctx() -> Context:
    return Context(config=Config(defaults=local.CONFIG))


@pytest.fixture
def dotenv(tmp_path) -> Generator[str, None, None]:
    tmp_file = tmp_path / "dotenv.tmpl"
    tmp_file.write_text("TEST=1")
    yield tmp_file.as_posix()


@pytest.fixture
def pods_config() -> types.PodsConfig:
    return {
        "test1": {
            "podNamespace": "default",
            "podPrefix": "test1-",
            "podPort": 80,
            "localPort": 8000,
        },
        "test2": {
            "podNamespace": "default",
            "podPrefix": "test2-",
            "podPort": 80,
            "localPort": 8000,
        },
        "test3": {
            "podNamespace": "default",
            "serviceName": "web",
            "podPort": 80,
            "localPort": 8000,
        },
    }


@pytest.fixture
def filtered_pods(pods_config) -> dict[str, str]:
    return dict(zip(pods_config.keys(), pods_config.keys()))


@pytest.fixture
def config(tmp_path, pods_config) -> Generator[str, None, None]:
    tmp_file = tmp_path / "config.json"
    tmp_file.write_text(json.dumps({"podForwards": pods_config}))
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
        with pytest.raises(exceptions.UndefinedVariable):
            local.ports(ctx)

    def test_raise_error_if_unknown_config(self, tmp_path, ctx):
        config = tmp_path / "config.json"

        with pytest.raises(exceptions.PathNotFound):
            local.ports(ctx, config=config.as_posix())

    def test_raise_error_if_incorrect_config(self, tmp_path, ctx):
        config = tmp_path / "config.json"
        config.write_text('{"podForwards": "test"}')

        with pytest.raises(exceptions.InvalidConfig):
            local.ports(ctx, config=config.as_posix())

    @pytest.mark.parametrize("unforward", [False, True])
    def test_raise_error_if_missing_pod(self, mocker, ctx, config, unforward):
        with pytest.raises(exceptions.UndefinedVariable):
            local.ports(ctx, config=config, pod="test", unforward=unforward)

    @pytest.mark.parametrize("unforward", [False, True])
    @pytest.mark.parametrize("pod", [None, "test1", "test2", "test3"])
    def test_execute_correct_kubectl_commands(
        self, mocker, ctx, pods_config, filtered_pods, config, pod, unforward
    ):
        mocked_filter = mocker.patch.object(local, "_filter_pods", return_value=filtered_pods)
        mocked_forward = mocker.patch.object(local, "_forward")
        mocked_unforward = mocker.patch.object(local, "_unforward")

        local.ports(ctx, config=config, pod=pod, unforward=unforward)

        mocked_filter.assert_called_once()

        if unforward:
            if pod:
                mocked_unforward.assert_called_with(ctx, pods_config[pod])
            else:
                mocked_unforward.call_args_list == [
                    (ctx, pods_config["test1"]),
                    (ctx, pods_config["test2"]),
                ]
        else:
            if pod:
                mocked_forward.assert_called_with(ctx, pods_config[pod], pod)
            else:
                mocked_forward.call_args_list == [
                    (ctx, pods_config["test1"], "test1"),
                    (ctx, pods_config["test2"], "test2"),
                ]
