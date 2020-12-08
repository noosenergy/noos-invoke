import pytest
from invoke import context

from noos_ci import python, utils


@pytest.fixture
def ctx():
    return context.Context(config=python.CONFIG)


class TestInstallType:
    def test_unknown_install_type_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            python.InstallType.get(ctx, "bad_install")


class TestPythonTest:
    def test_incorrect_group_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            python.test(ctx, group="bad_group")

    @pytest.mark.parametrize("group", ["unit", "integration", "functional"])
    def test_invalid_path_raises_error(self, group, ctx):
        with pytest.raises(utils.PathNotFound):
            python.test(ctx, tests="bad_path", group=group)


class TestPythonRelease:
    def test_pipenv_release_raises_error(self, ctx):
        with pytest.raises(NotImplementedError):
            python.release(ctx, user="test_user", token="test_token", install="pipenv")
