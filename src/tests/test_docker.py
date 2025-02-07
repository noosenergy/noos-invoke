from collections.abc import Generator

import pytest
from invoke import Config, Context

from noos_inv import docker, utils


@pytest.fixture
def ctx() -> Context:
    return Context(config=Config(defaults=docker.CONFIG))


@pytest.fixture
def image_context(tmp_path) -> Generator[str, None, None]:
    yield tmp_path.as_posix()


@pytest.fixture
def image_file(tmp_path) -> Generator[str, None, None]:
    tmp_file = tmp_path / "Dockerfile"
    tmp_file.write_text("FROM python:3.8")
    yield tmp_file.as_posix()


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

        test_run.assert_called_with(cmd)

    def test_fetch_dockerhub_command_correctly(self, test_run, ctx):
        cmd = "docker login --username other_user --password test_token"

        docker.login(ctx, user="other_user", token="test_token")

        test_run.assert_called_with(cmd)


class TestDockerBuild:
    def test_invalid_context_raises_error(self, ctx):
        with pytest.raises(utils.PathNotFound):
            docker.build(ctx, context="bad_context")

    def test_missing_environment_variable_raises_error(self, ctx, image_context, image_file):
        with pytest.raises(AssertionError):
            docker.build(ctx, context=image_context, arg="BAD_VARIABLE")

    def test_fetch_command_correctly(self, test_run, ctx, image_context, image_file):
        cmd = f"docker build --pull --file {image_file} --tag test-image {image_context}"

        docker.build(ctx, name="test-image", context=image_context)

        test_run.assert_called_with(cmd)

    def test_fetch_command_correctly_with_file(self, test_run, ctx, image_context, image_file):
        cmd = f"docker build --pull --file {image_file} --tag test-image {image_context}"

        docker.build(ctx, name="test-image", file=image_file, context=image_context)

        test_run.assert_called_with(cmd)

    def test_fetch_command_correctly_with_build_args(
        self, monkeypatch, test_run, ctx, image_context, image_file
    ):
        monkeypatch.setenv("TEST_VARIABLE", "test_value")
        cmd = (
            f"docker build --pull --file {image_file} --tag test-image "
            f"--build-arg TEST_VARIABLE=test_value "
            f"{image_context}"
        )

        docker.build(ctx, name="test-image", context=image_context, arg="TEST_VARIABLE")

        test_run.assert_called_with(cmd)


class TestDockerBuildx:
    def test_invalid_context_raises_error(self, ctx):
        with pytest.raises(utils.PathNotFound):
            docker.buildx(ctx, context="bad_context")

    def test_missing_environment_variable_raises_error(self, ctx, image_context, image_file):
        with pytest.raises(AssertionError):
            docker.buildx(ctx, context=image_context, arg="BAD_VARIABLE")

    @pytest.mark.parametrize("image_platfom", ["linux/arm64", "linux/arm64,linux/amd64"])
    def test_fetch_command_correctly_with_platform(
        self, test_run, ctx, image_context, image_file, image_platfom
    ):
        cmd = (
            f"docker buildx build --pull --file {image_file} --tag test-repo/test-image:latest "
            f"--platform {image_platfom} --push {image_context}"
        )

        docker.buildx(
            ctx,
            repo="test-repo",
            name="test-image",
            file=image_file,
            context=image_context,
            platform=image_platfom,
        )

        test_run.assert_called_with(cmd)


class TestDockerPush:
    def test_fetch_command_correctly(self, test_run, ctx):
        cmd = "docker push test-repo/test-image:latest"

        docker.push(ctx, repo="test-repo", name="test-image")

        assert test_run.call_count == 4
        test_run.assert_called_with(cmd)

    def test_fetch_dry_run_command_correctly(self, test_run, ctx):
        cmd = "docker tag test-image test-repo/test-image:latest"

        docker.push(ctx, repo="test-repo", name="test-image", dry_run=True)

        assert test_run.call_count == 2
        test_run.assert_called_with(cmd)

    def test_fetch_tag_only_command_correctly(self, test_run, ctx):
        cmd = "docker push test-repo/test-image:1.0"

        docker.push(ctx, repo="test-repo", name="test-image", tag=1.0, tag_only=True)

        assert test_run.call_count == 2
        test_run.assert_called_with(cmd)

    def test_fetch_dry_run_tag_only_command_correctly(self, test_run, ctx):
        cmd = "docker tag test-image test-repo/test-image:1.0"

        docker.push(ctx, repo="test-repo", name="test-image", tag=1.0, dry_run=True, tag_only=True)

        assert test_run.call_count == 1
        test_run.assert_called_with(cmd)
