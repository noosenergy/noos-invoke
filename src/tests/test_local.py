from collections.abc import Generator

import pytest
from invoke import Context

from noos_inv import local


@pytest.fixture
def ctx() -> Context:
    return Context()


@pytest.fixture
def dotenv(tmp_path) -> Generator[str, None, None]:
    tmp_file = tmp_path / "dotenv.tmpl"
    tmp_file.write_text("TEST=1")
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
