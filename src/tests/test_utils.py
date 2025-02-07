import pytest

from noos_inv import utils


class TestCheckPath:
    def test_invalid_path_raises_error(self):
        with pytest.raises(utils.PathNotFound):
            utils.check_path("invalid/path")

    def test_valid_path_passes_silently(self, tmp_path):
        utils.check_path(tmp_path.as_posix())
