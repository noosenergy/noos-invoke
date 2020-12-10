[![CircleCI](https://circleci.com/gh/noosenergy/noos-deploy.svg?style=svg&circle-token=68d1a71e4f53ab1a1f33110e9a8c24bd3300a8ba)](https://circleci.com/gh/noosenergy/noos-deploy)

# Noos Deploy

Software development kit for sharing workflows across CI/CD pipelines.

## Installation

Package available from the [PyPi repository](https://pypi.org/project/noos-ci/):

    $ pip install noos-ci

## Usage as a command line tool

The `noos-ci` package exposes a command line interface, for managing common CI/CD tasks.

Such a project aims to enforce parity between development and CI/CD workflows, ensuring reproducability in local and remote containers (e.g. executable versions, command line calls, environment variables...).

From the terminal,

```shell
$ noosci

Usage: noosci [--core-opts] <subcommand> [--subcommand-opts] ...

Subcommands:

  docker.build       Build Docker image locally.
  docker.login       Login to Docker remote registry (AWS ECR or Dockerhub).
  docker.push        Push Docker image to a remote registry.
  git.config         Setup git credentials with a Github token.
  helm.install       Provision local Helm client (Chart Museum Plugin).
  helm.lint          Check compliance of Helm charts / values.
  helm.login         Login to Helm remote registry (Chart Museum).
  helm.push          Push Helm chart to a remote registry.
  helm.test          Test local deployment in Minikube.
  local.dotenv       Create local dotenv file.
  python.clean       Clean project from temp files / dirs.
  python.format      Auto-format source code.
  python.lint        Run python linters.
  python.package     Build project wheel distribution.
  python.release     Publish wheel distribution to PyPi.
  python.test        Run pytest with optional grouped tests.
  terraform.run      Run a plan in Terraform cloud.
  terraform.update   Update variable in Terraform cloud.
```

## Development

On Mac OSX, make sure [poetry](https://python-poetry.org/) has been installed and pre-configured,

    $ brew install poetry

This project is shipped with a Makefile, which is ready to do basic common tasks.

```shell
$ make

help                           Display this auto-generated help message
clean                          Clean project from temp files / dirs
format                         Run auto-formatting linters
lint                           Run python linters
test                           Run pytest with all tests
package                        Build project wheel distribution
release                        Publish wheel distribution to PyPi
```
