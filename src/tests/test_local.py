from invoke import context

from noos_ci import local, utils


def test_force_replace_dotenv(mocker):
    mocker.patch.object(utils, "check_path")
    mocked_run = mocker.patch.object(context.Context, "run")

    local.dotenv(context.Context(), force=True)

    mocked_run.assert_called_once()
