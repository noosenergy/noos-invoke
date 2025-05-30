from collections.abc import Generator

import pytest
from invoke import Config, Context

from noos_inv import exceptions
from noos_inv.tasks import helm


@pytest.fixture
def ctx() -> Context:
    return Context(config=Config(defaults=helm.CONFIG))


@pytest.fixture
def chart(tmp_path) -> Generator[str, None, None]:
    yield tmp_path.as_posix()


class TestHelmLogin:
    @pytest.mark.parametrize(
        "url,token",
        [
            (None, None),
            ("http://hostname/", None),
        ],
    )
    def test_raise_error_if_no_chartmuseum_secrets(self, url, token, ctx):
        with pytest.raises(exceptions.UndefinedVariable):
            helm.login(ctx, url=url, user="other_user", token=token)

    def test_fetch_aws_command_correctly(self, test_run, ctx):
        cmd = (
            "aws ecr get-login-password | "
            "helm registry login --username AWS --password-stdin test.repo"
        )

        helm.login(ctx, repo="test.repo", user="AWS")

        test_run.assert_called_with(cmd)

    def test_fetch_chartmuseum_command_correctly(self, test_run, ctx):
        cmd = "helm repo add test-repo http://hostname --username other_user --password test-token"

        helm.login(
            ctx, repo="test-repo", url="http://hostname", user="other_user", token="test-token"
        )

        test_run.assert_called_with(cmd)


class TestHelmInstall:
    def test_fetch_command_correctly(self, test_run, ctx):
        cmd = "helm plugin install http://hostname"

        helm.install(ctx, plugins=["http://hostname"])

        test_run.assert_called_with(cmd)


class TestHelmLint:
    def test_raise_error_if_invalid_chart(self, ctx):
        with pytest.raises(exceptions.PathNotFound):
            helm.lint(ctx, chart="bad_chart")

    def test_fetch_command_correctly(self, test_run, ctx, chart):
        cmd = f"helm lint {chart}"

        helm.lint(ctx, chart=chart)

        test_run.assert_called_with(cmd)


class TestHelmPush:
    def test_raise_error_if_invalid_chart(self, ctx):
        with pytest.raises(exceptions.PathNotFound):
            helm.push(ctx, chart="bad_chart")

    def test_fetch_aws_command_correctly(self, chart, test_run, ctx):
        cmd = "helm push chart-latest.tgz oci://test.repo/local/test"

        helm.push(ctx, chart=chart, repo="test.repo", name="local/test/chart", tag="latest")

        test_run.assert_called_with(cmd)

    def test_fetch_chartmuseum_command_correctly(self, test_run, chart):
        cfg = helm.CONFIG
        cfg["helm"]["user"] = "other_user"
        ctx = Context(config=Config(defaults=cfg))
        cmd = f"helm cm-push {chart} test-repo"

        helm.push(ctx, chart=chart, repo="test-repo")

        test_run.assert_called_with(cmd)

    def test_fetch_chartmuseum_command_correctly_with_dry_run(self, test_run, chart):
        cfg = helm.CONFIG
        cfg["helm"]["user"] = "other_user"
        ctx = Context(config=Config(defaults=cfg))
        cmd = f"helm dependency update {chart}"

        helm.push(ctx, chart=chart, repo="test-repo", dry_run=True)

        test_run.assert_called_with(cmd)
