import tempfile

import pytest

from noos_inv import utils


@pytest.fixture
def path():
    with tempfile.TemporaryDirectory() as dir_name:
        yield dir_name


class TestCheckPath:
    def test_invalid_path_raises_error(self):
        with pytest.raises(utils.PathNotFound):
            utils.check_path("invalid/path")

    def test_valid_path_passes_silently(self, path):
        utils.check_path(path)
