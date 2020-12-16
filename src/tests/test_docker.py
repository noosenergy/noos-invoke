import tempfile

import pytest
from invoke import context

from noos_ci import docker, utils


@pytest.fixture
def ctx():
    return context.Context(config=docker.CONFIG)


@pytest.fixture
def image_context():
    with tempfile.TemporaryDirectory() as dir_name:
        yield dir_name


class TestDockerLogin:
    def test_no_aws_repo_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            docker.login(ctx, user="AWS")

    def test_no_dockerhub_token_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            docker.login(ctx, user="other_user")

    def test_fetch_aws_command_correctly(self, test_run, ctx):
        cmd = (
            "aws ecr get-login-password | "
            "docker login --username AWS --password-stdin http://hostname/repo"
        )

        docker.login(ctx, repo="http://hostname/repo", user="AWS")

        test_run.assert_called_with(cmd, pty=True)

    def test_fetch_dockerhub_command_correctly(self, test_run, ctx):
        cmd = "docker login --username other_user --password test_token"

        docker.login(ctx, user="other_user", token="test_token")

        test_run.assert_called_with(cmd, pty=True)


class TestDockerBuild:
    def test_invalid_context_raises_error(self, ctx):
        with pytest.raises(utils.PathNotFound):
            docker.build(ctx, context="bad_context")

    def test_missing_environment_variable_raises_error(self, ctx, image_context):
        with pytest.raises(AssertionError):
            docker.build(ctx, context=image_context, arg="BAD_VARIABLE")

    def test_fetch_command_correctly(self, test_run, ctx, image_context):
        cmd = f"docker build --pull --tag test-image {image_context}"

        docker.build(ctx, name="test-image", context=image_context)

        test_run.assert_called_with(cmd, pty=True)

    def test_fetch_command_correctly_with_build_args(
        self, monkeypatch, test_run, ctx, image_context
    ):
        monkeypatch.setenv("TEST_VARIABLE", "test_value")
        cmd = (
            f"docker build --pull --tag test-image "
            f"--build-arg TEST_VARIABLE=test_value "
            f"{image_context}"
        )

        docker.build(ctx, name="test-image", context=image_context, arg="TEST_VARIABLE")

        test_run.assert_called_with(cmd, pty=True)


class TestDockerPush:
    def test_fetch_dry_run_command_correctly(self, test_run, ctx):
        cmd = "docker tag test-image test-repo/test-image:latest"

        docker.push(ctx, repo="test-repo", name="test-image", dry_run=True)

        test_run.assert_called_with(cmd, pty=True)
