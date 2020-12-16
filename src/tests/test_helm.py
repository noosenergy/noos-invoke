import pytest
from invoke import context

from noos_ci import helm, utils


@pytest.fixture
def ctx():
    return context.Context(config=helm.CONFIG)


class TestHelmLogin:
    def test_missing_token_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            helm.login(ctx)

    def test_fetch_command_correctly(self, test_run, ctx):
        cmd = (
            "helm repo add test_repo http://hostname/ "
            "--username test_user --password test-token"
        )

        helm.login(
            ctx, repo="test_repo", url="http://hostname/", user="test_user", token="test-token"
        )

        test_run.assert_called_with(cmd, pty=True)


class TestHelmLint:
    def test_invalid_chart_raises_error(self, ctx):
        with pytest.raises(utils.PathNotFound):
            helm.lint(ctx, chart="bad_chart")


class TestHelmPush:
    def test_invalid_chart_raises_error(self, ctx):
        with pytest.raises(utils.PathNotFound):
            helm.push(ctx, chart="bad_chart")
