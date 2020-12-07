import pytest
from invoke import context

from noos_ci import docker, utils


@pytest.fixture
def ctx():
    return context.Context(config=docker.CONFIG)


class TestLogin:
    def test_invalid_user_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            docker.login(ctx, user="bad_user")

    def test_no_aws_repo_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            docker.login(ctx, user="AWS")

    def test_no_dockerhub_token_raises_error(self, ctx):
        with pytest.raises(AssertionError):
            docker.login(ctx, user="noosenergy")


class TestBuild:
    def test_invalid_context_raises_error(self, ctx):
        with pytest.raises(utils.PathNotFound):
            docker.build(ctx, context="bad_context")
