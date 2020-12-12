import pytest
from invoke import Context


# Invoke fixture:


@pytest.fixture(scope="function")
def test_run(mocker):
    """Mock `invoke`'s context behaviour."""
    return mocker.patch.object(Context, "run")
