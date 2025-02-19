import pytest

from noos_inv import types


@pytest.mark.parametrize(
    "enum_class",
    [
        types.InstallType,
        types.GroupType,
        types.FormatterType,
        types.LinterType,
    ],
)
class TestValidatedEnum:
    def test_raise_error_for_unknown_install(self, enum_class):
        with pytest.raises(AssertionError):
            enum_class.get("bad_install")

    def test_retrieve_registered_install_correctly(self, enum_class):
        for enum_type in enum_class:
            assert enum_class.get(str(enum_type).lower()) == enum_type
