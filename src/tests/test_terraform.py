import pytest
from invoke import context

from noos_ci import terraform


@pytest.fixture
def ctx():
    return context.Context(config=terraform.CONFIG)


class TestTerraformUpdate:
    def test_missing_token_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            terraform.update(ctx)

    def test_fetch_command_correctly(self, test_run, ctx):
        cmd = (
            "noostf update --variable myVariable --value 'myValue' "
            "--organisation noosenergy --workspace noos-prod --token test-token"
        )

        terraform.update(ctx, variable="myVariable", value="myValue", token="test-token")

        test_run.assert_called_with(cmd, pty=True)


class TestTerraformRun:
    def test_missing_token_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            terraform.run(ctx)

    def test_fetch_command_correctly(self, test_run, ctx):
        cmd = (
            "noostf run --message 'myMessage' "
            "--organisation noosenergy --workspace noos-prod --token test-token"
        )

        terraform.run(ctx, message="myMessage", token="test-token")

        test_run.assert_called_with(cmd, pty=True)
