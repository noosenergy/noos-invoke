import tempfile

import pytest
from invoke import context

from noos_inv import helm, utils


@pytest.fixture
def ctx():
    return context.Context(config=helm.CONFIG)


@pytest.fixture
def chart():
    with tempfile.TemporaryDirectory() as dir_name:
        yield dir_name


class TestHelmLogin:
    @pytest.mark.parametrize(
        "url,user,token",
        [
            (None, None, None),
            ("http://hostname/", None, None),
            ("http://hostname/", "test_user", None),
        ],
    )
    def test_missing_secret_raises_error(self, url, user, token, ctx):
        with pytest.raises(AssertionError):
            helm.login(ctx, url=url, user=user, token=token)

    def test_fetch_command_correctly(self, test_run, ctx):
        cmd = (
            "helm repo add test_repo http://hostname/ "
            "--username test_user --password test-token"
        )

        helm.login(
            ctx, repo="test_repo", url="http://hostname/", user="test_user", token="test-token"
        )

        test_run.assert_called_with(cmd)


class TestHelmInstall:
    def test_fetch_command_correctly(self, test_run, ctx):
        cmd = "helm plugin install http://hostname/"

        helm.install(ctx, plugins=["http://hostname/"])

        test_run.assert_called_with(cmd)


class TestHelmLint:
    def test_invalid_chart_raises_error(self, ctx):
        with pytest.raises(utils.PathNotFound):
            helm.lint(ctx, chart="bad_chart")

    def test_fetch_command_correctly(self, test_run, ctx, chart):
        cmd = f"helm lint {chart}"

        helm.lint(ctx, chart=chart)

        test_run.assert_called_with(cmd)


class TestHelmPush:
    def test_invalid_chart_raises_error(self, ctx):
        with pytest.raises(utils.PathNotFound):
            helm.push(ctx, chart="bad_chart")

    def test_fetch_command_correctly(self, test_run, ctx, chart):
        cmd = f"helm cm-push {chart} test_repo"

        helm.push(ctx, chart=chart, repo="test_repo")

        test_run.assert_called_with(cmd)
