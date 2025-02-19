import pytest

from noos_inv import exceptions, validators


class TestCheckPath:
    def test_raise_error_if_invalid_path(self):
        with pytest.raises(exceptions.PathNotFound):
            validators.check_path("invalid/path")

    def test_pass_silently_for_valid_path(self, tmp_path):
        validators.check_path(tmp_path.as_posix())


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
    def test_raise_error_if_invalid_schema(self, config):
        with pytest.raises(exceptions.InvalidConfig):
            validators.check_config(config)

    @pytest.mark.parametrize(
        "config",
        [
            {
                "test": {
                    "podNamespace": "default",
                    "podPrefix": "test-",
                    "podPort": 80,
                    "localPort": 8080,
                }
            },
            {
                "test": {
                    "podNamespace": "default",
                    "podPrefix": "test-",
                    "podPort": 80,
                    "localAddress": "0.0.0.0",
                    "localPort": 8080,
                }
            },
        ],
    )
    def test_pass_silently_for_valid_schema(self, config):
        validators.check_config(config)
