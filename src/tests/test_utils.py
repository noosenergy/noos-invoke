import pytest

from noos_inv import utils


class TestCheckPath:
    def test_invalid_path_raises_error(self):
        with pytest.raises(utils.PathNotFound):
            utils.check_path("invalid/path")

    def test_valid_path_passes_silently(self, tmp_path):
        utils.check_path(tmp_path.as_posix())


class TestCheckSchema:
    @pytest.mark.parametrize(
        "config",
        [
            None,
            ["invalid", "schema"],
            {"valid": ["invalid", "schema"]},
            {"valid": {"invalid": "schema"}},
            {"valid": {"podPrefix": "test-", "podPort": 80, "localPort": 8080}},
        ],
    )
    def test_invalid_schema_raises_error(self, config):
        with pytest.raises(utils.ValidationError):
            utils.check_schema(config)

    def test_valid_schema_passes_silently(self):
        config = {
            "test": {
                "podNamespace": "default",
                "podPrefix": "test-",
                "podPort": 80,
                "localPort": 8080,
            }
        }

        utils.check_schema(config)
