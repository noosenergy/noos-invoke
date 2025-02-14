import pytest
from invoke import Config, Context

from noos_inv import terraform


@pytest.fixture
def ctx() -> Context:
    return Context(config=Config(defaults=terraform.CONFIG))


class TestTerraformUpdate:
    @pytest.mark.parametrize(
        "organisation,workspace,token",
        [
            (None, None, None),
            ("test-organisation", None, None),
            ("test-organisation", "test-workspace", None),
        ],
    )
    def test_raise_error_if_missing_secret(self, organisation, workspace, token, ctx):
        with pytest.raises(AssertionError):
            terraform.update(ctx, organisation=organisation, workspace=workspace, token=token)

    def test_fetch_command_correctly(self, test_run, ctx):
        cmd = (
            "noostf update --variable myVariable --value 'myValue' "
            "--organisation test-organisation --workspace test-workspace --token test-token"
        )

        terraform.update(
            ctx,
            variable="myVariable",
            value="myValue",
            organisation="test-organisation",
            workspace="test-workspace",
            token="test-token",
        )

        test_run.assert_called_with(cmd, pty=True)


class TestTerraformRun:
    @pytest.mark.parametrize(
        "organisation,workspace,token",
        [
            (None, None, None),
            ("test-organisation", None, None),
            ("test-organisation", "test-workspace", None),
        ],
    )
    def test_raise_error_if_missing_secret(self, ctx, organisation, workspace, token):
        with pytest.raises(AssertionError):
            terraform.run(ctx, organisation=organisation, workspace=workspace, token=token)

    def test_fetch_command_correctly(self, test_run, ctx):
        cmd = (
            "noostf run --message 'myMessage' "
            "--organisation test-organisation --workspace test-workspace --token test-token"
        )

        terraform.run(
            ctx,
            message="myMessage",
            organisation="test-organisation",
            workspace="test-workspace",
            token="test-token",
        )

        test_run.assert_called_with(cmd, pty=True)
