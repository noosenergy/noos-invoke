import tempfile

import pytest
from invoke import Context

from noos_inv import local


@pytest.fixture
def ctx() -> Context:
    return Context()


@pytest.fixture
def dotenv():
    with tempfile.NamedTemporaryFile(mode="w+t") as dir_file:
        yield dir_file.name


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
