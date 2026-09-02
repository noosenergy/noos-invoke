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
    (tmp_path / "Chart.yaml").write_text("version: 2.3.4\n")
    yield tmp_path.as_posix()


@pytest.fixture
def values(tmp_path) -> Generator[str, None, None]:
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

    def test_fetch_command_correctly(self, test_run, ctx, chart, values):
        cmd = f"helm template {chart} --values {values}"

        helm.lint(ctx, chart=chart, values=values)

        assert test_run.call_count == 2
        assert cmd in test_run.call_args[0][0]


class TestHelmPush:
    @pytest.mark.parametrize(
        "chart,manifest,error",
        [
            pytest.param("bad_chart", None, exceptions.PathNotFound, id="incorrect-folder"),
            pytest.param(None, None, exceptions.PathNotFound, id="missing-manifest"),
            pytest.param(
                None,
                "name: local/test/chart\n",
                exceptions.UndefinedVariable,
                id="missing-version",
            ),
        ],
    )
    def test_raise_error_if_invalid_chart(self, tmp_path, ctx, chart, manifest, error):
        chart = chart or tmp_path.as_posix()
        if manifest is not None:
            (tmp_path / "Chart.yaml").write_text(manifest)

        with pytest.raises(error):
            helm.push(ctx, chart=chart, repo="test.repo")

    def test_fetch_aws_command_correctly_with_chart_version(self, test_run, ctx, chart):
        cmd = "helm push chart-2.3.4.tgz oci://test.repo/local/test"

        helm.push(ctx, chart=chart, repo="test.repo", name="local/test/chart")

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
