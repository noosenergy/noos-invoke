[![CircleCI](https://circleci.com/gh/noosenergy/noos-ci.svg?style=svg&circle-token=68d1a71e4f53ab1a1f33110e9a8c24bd3300a8ba)](https://circleci.com/gh/noosenergy/noos-ci)

# Noos Deploy

Shared workflows across CI/CD pipelines

## Quickstart

### Docker installation

On Mac OSX, make sure [poetry](https://python-poetry.org/) has been installed and pre-configured,

    $ brew install poetry

### Local development

This project is relying on its own shipped CLI, for common CI/CD tasks.

```
$ nooci
Usage: noosci [--core-opts] <subcommand> [--subcommand-opts] ...

Core options:

  --complete                         Print tab-completion candidates for given parse remainder.
  --hide=STRING                      Set default value of run()'s 'hide' kwarg.
  --print-completion-script=STRING   Print the tab-completion script for your preferred shell
                                     (bash|zsh|fish).
  --prompt-for-sudo-password         Prompt user at start of session for the sudo.password config value.
  --write-pyc                        Enable creation of .pyc files.
  -d, --debug                        Enable debug output.
  -D INT, --list-depth=INT           When listing tasks, only show the first INT levels.
  -e, --echo                         Echo executed commands before running.
  -f STRING, --config=STRING         Runtime configuration file to use.
  -F STRING, --list-format=STRING    Change the display format used when listing tasks. Should be one of:
                                     flat (default), nested, json.
  -h [STRING], --help[=STRING]       Show core or per-task help and exit.
  -l [STRING], --list[=STRING]       List available tasks, optionally limited to a namespace.
  -p, --pty                          Use a pty when executing shell commands.
  -R, --dry                          Echo commands instead of running.
  -T INT, --command-timeout=INT      Specify a global command execution timeout, in seconds.
  -V, --version                      Show version and exit.
  -w, --warn-only                    Warn, instead of failing, when shell commands fail.

Subcommands:

  dev.dotenv     Create local dotenv file.
  docker.build   Build Docker image locally.
  docker.login   Login to Docker remote registry (AWS ECR or Dockerhub).
  docker.push    Push Docker image to a remote registry.
  git.config     Setup git credentials with a Github token.
  helm.install   Provision local Helm client (Chart Museum Plugin).
  helm.lint      Check compliance of Helm charts / values.
  helm.login     Login to Helm remote registry (Chart Museum).
  helm.push      Push Helm chart to a remote registry.
  helm.test      Test local deployment in Minikube.
  py.clean       Clean project from temp files / dirs.
  py.format      Auto-format source code.
  py.lint        Run python linters.
  py.package     Build project wheel distribution.
  py.release     Publish wheel distribution to PyPi.
  py.test        Run pytest with optional grouped tests.
```
