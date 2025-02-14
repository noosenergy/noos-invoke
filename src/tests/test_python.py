from collections.abc import Generator

import pytest
from invoke import Config, Context

from noos_inv import python, utils


@pytest.fixture
def ctx() -> Context:
    return Context(config=Config(defaults=python.CONFIG))


@pytest.fixture
def source(tmp_path) -> Generator[str, None, None]:
    yield tmp_path.as_posix()


@pytest.mark.parametrize(
    "enum_class",
    [
        python.InstallType,
        python.GroupType,
        python.FormatterType,
        python.LinterType,
    ],
)
class TestValidatedEnum:
    def test_raise_error_for_unknown_install(self, enum_class):
        with pytest.raises(AssertionError):
            enum_class.get("bad_install")

    def test_retrieve_registered_install_correctly(self, enum_class):
        for enum_type in enum_class:
            assert enum_class.get(str(enum_type).lower()) == enum_type


class TestPythonFormat:
    def test_raise_error_if_invalid_source(self, ctx):
        with pytest.raises(utils.PathNotFound):
            python.format(ctx, source="bad_src")

    def test_raise_error_if_unknown_formatter_type(self, ctx, source):
        with pytest.raises(AssertionError):
            python.format(ctx, source=source, formatters="bad_formatter")

    def test_fetch_command_correctly(self, test_run, ctx, source):
        cmd = f"pipenv run ruff format {source}"

        python.format(ctx, source=source, install="pipenv")

        assert test_run.call_count == 2
        test_run.assert_called_with(cmd)


class TestPythonLint:
    def test_raise_error_if_invalid_source(self, ctx):
        with pytest.raises(utils.PathNotFound):
            python.lint(ctx, source="bad_src")

    def test_raise_error_if_unknown_linter_type(self, ctx, source):
        with pytest.raises(AssertionError):
            python.lint(ctx, source=source, linters="bad_linter")

    def test_fetch_command_correctly(self, test_run, ctx, source):
        cmd = f"pipenv run mypy {source}"

        python.lint(ctx, source=source, install="pipenv", linters="black,isort,mypy")

        assert test_run.call_count == 3
        test_run.assert_called_with(cmd, pty=True)


class TestPythonTest:
    def test_raise_error_if_incorrect_group(self, ctx):
        with pytest.raises(AssertionError):
            python.test(ctx, group="bad_group")

    @pytest.mark.parametrize("group", ["unit", "integration", "functional"])
    def test_raise_error_if_invalid_source(self, group, ctx):
        with pytest.raises(utils.PathNotFound):
            python.test(ctx, tests="bad_path", group=group)

    @pytest.mark.parametrize("group", ["unit", "integration", "functional"])
    def test_fetch_command_correctly(self, tmp_path, test_run, ctx, group):
        (tmp_path / group).mkdir()
        cmd = f"pipenv run pytest {tmp_path / group}"

        python.test(ctx, tests=tmp_path.as_posix(), group=group, install="pipenv")

        test_run.assert_called_with(cmd, pty=True)


class TestPythonPackage:
    def test_raise_error_if_unknown_install_type(self, ctx):
        with pytest.raises(AssertionError):
            python.package(ctx, install="bad_install")

    @pytest.mark.parametrize(
        "install,cmd,pty",
        [
            ("pipenv", "pipenv run python -m build -n", True),
            ("poetry", "poetry build", True),
            ("uv", "uvx --from build pyproject-build --installer uv", False),
        ],
    )
    def test_fetch_command_correctly(self, install, cmd, pty, test_run, ctx):
        python.package(ctx, install=install)
        if pty:
            test_run.assert_called_with(cmd, pty=True)
        else:
            test_run.assert_called_with(cmd)


class TestPythonRelease:
    @pytest.mark.parametrize(
        "user,token",
        [
            (None, None),
            ("test_user", None),
        ],
    )
    def test_raise_error_if_missing_secret(self, user, token, ctx):
        with pytest.raises(AssertionError):
            python.release(ctx, user=user, token=token)

    def test_raise_error_if_unknown_install_type(self, ctx):
        with pytest.raises(AssertionError):
            python.release(ctx, user="test_user", token="test_token", install="bad_install")

    @pytest.mark.parametrize(
        "install,cmd,pty",
        [
            ("pipenv", "pipenv run twine upload dist/* -u test_user -p test_token", True),
            ("poetry", "poetry publish --build -u test_user -p test_token", True),
            ("uv", "uvx twine upload dist/* -u test_user -p test_token", False),
        ],
    )
    def test_fetch_command_correctly(self, install, cmd, pty, test_run, ctx):
        python.release(ctx, user="test_user", token="test_token", install=install)
        if pty:
            test_run.assert_called_with(cmd, pty=True)
        else:
            test_run.assert_called_with(cmd)
