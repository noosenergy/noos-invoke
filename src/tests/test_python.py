import tempfile

import pytest
from invoke import context

from noos_ci import python, utils


@pytest.fixture
def ctx():
    return context.Context(config=python.CONFIG)


@pytest.fixture
def source():
    with tempfile.TemporaryDirectory() as dir_name:
        yield dir_name


class TestInstallType:
    def test_unknown_install_type_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            python.InstallType.get(ctx, "bad_install")

    def test_retrieve_default_install_correctly(self, ctx):
        assert python.InstallType.get(ctx, None) == ctx.python.install


class TestPythonFormat:
    def test_invalid_source_raises_error(self, ctx):
        with pytest.raises(utils.PathNotFound):
            python.format(ctx, source="bad_src")

    def test_fetch_command_correctly(self, test_run, ctx, source):
        cmd = f"pipenv run isort {source}"

        python.format(ctx, source=source, install="pipenv")

        assert test_run.call_count == 2
        test_run.assert_called_with(cmd, pty=True)


class TestPythonLint:
    def test_invalid_source_raises_error(self, ctx):
        with pytest.raises(utils.PathNotFound):
            python.lint(ctx, source="bad_src")

    def test_fetch_command_correctly(self, test_run, ctx, source):
        cmd = f"pipenv run mypy {source}"

        python.lint(ctx, source=source, install="pipenv")

        assert test_run.call_count == 5
        test_run.assert_called_with(cmd, pty=True)


class TestPythonTest:
    def test_incorrect_group_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            python.test(ctx, group="bad_group")

    @pytest.mark.parametrize("group", ["unit", "integration", "functional"])
    def test_invalid_source_raises_error(self, group, ctx):
        with pytest.raises(utils.PathNotFound):
            python.test(ctx, tests="bad_path", group=group)

    def test_fetch_command_correctly(self, test_run, ctx, source):
        cmd = f"pipenv run pytest {source}"

        python.test(ctx, tests=source, install="pipenv")

        test_run.assert_called_with(cmd, pty=True)


class TestPythonPackage:
    def test_unknown_install_type_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            python.package(ctx, install="bad_install")

    @pytest.mark.parametrize(
        "install,cmd",
        [
            ("pipenv", "pipenv run python setup.py sdist"),
            ("poetry", "poetry build"),
        ],
    )
    def test_fetch_command_correctly(self, install, cmd, test_run, ctx):
        python.package(ctx, install=install)

        test_run.assert_called_with(cmd, pty=True)


class TestPythonRelease:
    @pytest.mark.parametrize(
        "user,token",
        [
            (None, None),
            ("test_user", None),
        ],
    )
    def test_missing_secret_raises_error(self, user, token, ctx):
        with pytest.raises(AssertionError):
            python.release(ctx, user=user, token=token)

    def test_unknown_install_type_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            python.release(ctx, user="test_user", token="test_token", install="bad_install")

    def test_pipenv_release_raises_error(self, ctx):
        with pytest.raises(NotImplementedError):
            python.release(ctx, user="test_user", token="test_token", install="pipenv")

    def test_fetch_command_correctly(self, test_run, ctx):
        cmd = "poetry publish --build -u test_user -p test_token"

        python.release(ctx, user="test_user", token="test_token", install="poetry")

        test_run.assert_called_with(cmd, pty=True)
