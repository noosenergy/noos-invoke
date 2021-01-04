import pytest
from invoke import context

from noos_ci import terraform


@pytest.fixture
def ctx():
    return context.Context(config=terraform.CONFIG)


class TestTerraformUpdate:
    @pytest.mark.parametrize(
        "organisation,workspace,token",
        [
            (None, None, None),
            ("test-organisation", None, None),
            ("test-organisation", "test-workspace", None),
        ],
    )
    def test_missing_secret_raises_error(self, organisation, workspace, token, ctx):
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
    def test_missing_secret_raises_error(self, ctx, organisation, workspace, token):
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
