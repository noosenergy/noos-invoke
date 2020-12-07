import pytest
from invoke import context

from noos_ci import py, utils


@pytest.fixture
def ctx():
    return context.Context(config=py.CONFIG)


class TestPythonTest:
    def test_incorrect_group_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            py.test(ctx, group="bad_group")

    @pytest.mark.parametrize("group", ["unit", "integration", "functional"])
    def test_invalid_path_raises_error(self, group, ctx):
        with pytest.raises(utils.PathNotFound):
            py.test(ctx, tests="bad_path", group=group)
