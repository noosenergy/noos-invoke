[![CircleCI](https://circleci.com/gh/noosenergy/noos-invoke.svg?style=svg&circle-token=5b4d9fc54d8987081b7c4a9a79fa8b436e70930c)](https://circleci.com/gh/noosenergy/noos-invoke)

# Noos Invoke

Software development kit for sharing workflows across CI/CD pipelines.

Such a project aims to enforce parity and reproducability between local development and CI/CD workflows in remote containers (e.g. executable versions, command line calls, environment variables...) - developped with `inv[oke]`(https://github.com/pyinvoke/invoke).

## Installation

Install the package from the [PyPi repository](https://pypi.org/project/noos-inv/):

    $ pip install noos-inv

To enable shell completion, execute the following command (e.g. `zsh`),

    $ noosinv --print-completion-script=zsh

And copy/paste its `stdout` into your shell config.

```bash
# NOOSINV completion script

_complete_noosinv() {
    collection_arg=''
    if [[ "${words}" =~ "(-c|--collection) [^ ]+" ]]; then
        collection_arg=$MATCH
    fi
    reply=( $(noosinv ${=collection_arg} --complete -- ${words}) )
}

compctl -K _complete_noosinv + -f noosinv
```

Finally, still in your shell config, enable automatic sub shell loading:

```bash
# ENV variable sub shell loading with command "source .env"

set -a
```

## Usage as a command line tool

The `noos-inv` package installs a CLI binary, for managing common CI/CD tasks.

From the terminal,

```
$ noosinv

Usage: noosinv [--core-opts] <subcommand> [--subcommand-opts] ...

Subcommands:

  docker.build       Build Docker image locally.
  docker.login       Login to Docker remote registry (AWS ECR or Dockerhub).
  docker.push        Push Docker image to a remote registry.
  docker.buildx      Build and push cross platform Docker image to a remote registry.
  git.config         Setup git credentials with a Github token.
  helm.install       Provision local Helm client (Chart Museum Plugin).
  helm.lint          Check compliance of Helm charts / values.
  helm.login         Login to Helm remote registry (Chart Museum).
  helm.push          Push Helm chart to a remote registry.
  helm.test          Test local deployment in Minikube.
  local.dotenv       Create local dotenv file.
  python.clean       Clean project from temp files / dirs.
  python.coverage    Run coverage test report.
  python.format      Auto-format source code.
  python.lint        Run python linters.
  python.package     Build project wheel distribution.
  python.release     Publish wheel distribution to PyPi.
  python.test        Run pytest with optional grouped tests.
  terraform.run      Run a plan in Terraform cloud.
  terraform.update   Update variable in Terraform cloud.
```

Source your environnement variables first for a seamless experience.
(use command `local.dotenv` to create it from the provided template)

    $ source .env

## Development

On Mac OSX, make sure [poetry](https://python-poetry.org/) has been installed and pre-configured,

    $ brew install poetry

This project is shipped with a Makefile, which is ready to do basic common tasks.

```
$ make

help                           Display this auto-generated help message
update                         Lock and install build dependencies
clean                          Clean project from temp files / dirs
format                         Run auto-formatting linters
install                        Install build dependencies from lock file
lint                           Run python linters
test                           Run pytest with all tests
package                        Build project wheel distribution
release                        Publish wheel distribution to PyPi
```
