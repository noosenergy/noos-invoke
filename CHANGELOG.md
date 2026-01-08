# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.0.1-alpha] - 2020-12-02
### Added
 - Initial release.
 - Common CI/CD tasks for basic Python, Docker and Helm workflows.

## [0.0.1-alpha.1] - 2020-12-02
### Added
 - Configure collections with default values.

## [0.0.1-alpha.2] - 2020-12-03
### Changed
 - New Helm and Docker collection configuration.
 - Better tasks args for the Python collection.

## [0.0.1-alpha.3] - 2020-12-03
### Changed
 - Allow login to either AWS ECR or Dockerhub.
 - Enforce test chart deployment into minikube.

## [0.0.1-alpha.4] - 2020-12-07
### Changed
 - Change OS env var prefix to `NOOSCI_` instead of `INVOKE_`.
 - Initialize sensitive config values to `None`.

## [0.0.1-alpha.5] - 2020-12-08
### Added
 - Split CircleCI workflow between testing and publishing.
 - Add a package manager field to run Python tasks within a venv.

## [0.0.1-alpha.6] - 2020-12-09
### Added
 - Add CI/CD tasks for basic Terraform workflow.

## [0.0.1] - 2020-12-10
### Added
 - First production release.

## [0.0.2] - 2020-12-10
### Changed
 - Small breadcrumbs left behind...

## [0.0.3] - 2020-12-17
### Added
 - Add Python task to generate test coverage reports.
 - Add Docker task to inject environment variables as build arguments.
 - Generally improve tasks test coverage.

## [0.0.4] - 2020-12-17
### Changed
 - Push Helm chart packaged up with their dependencies by default.

## [0.0.5] - 2021-01-04
### Changed
 - Rename project binary and python package `noos-inv` in relation with `inv[oke]`.

## [0.0.6] - 2021-01-05
### Changed
 - Bump Python version to v3.8.6.

## [0.0.7] - 2021-05-21
### Changed
 - Pass optional `--file` argument to command docker.build.

## [0.0.8] - 2021-10-07
### Changed
 - Update `helm.push` cmd to work with new chartmuseum plugin version 0.10.0
   and new helm version 3.7

## [0.0.9] - 2022-08-31
### Changed
 - Update `helm.push` cmd to work with Helm OCI registry functionality
   (available from helm version 3.8)

## [0.0.10] - 2022-09-05
### Changed
 - Allow pushing Helm charts to AWS ECR with bespoke tags.

## [0.0.11] - 2022-11-09
### Changed
 - Switch to module `build` to package Python librairies with `pipenv`.

## [0.0.12] - 2023-08-07
### Changed
 - Bump Python version to v3.11.4.

## [0.0.13] - 2023-09-18
### Changed
 - Bump Poetry version to v1.5.1.

## [0.0.14] - 2023-11-17
### Added
 - Add docker.buildx to build and push multi-platform images.

## [0.0.15] - 2023-11-20
### Added
 - Add buildx command to the docker tasks.

## [0.0.16] - 2023-11-23
### Added
 - Ensure build+push/buildx have the same workflow locally.

## [0.0.17] - 2023-11-28
### Added
 - Provision builder through `docker.configure` for multi-platform images.

## [0.0.18] - 2024-08-21
### Added
 - Add support for the `uv` python package manager.

## [0.0.19] - 2025-01-13
### Changed
 - Bump Python version to v3.12.8.

## [0.2.0] - 2025-01-27
### Changed
 - Allow a specific formatter or linter in `python.format` and `python.lint`.

## [0.2.1] - 2025-01-29
### Changed
 - Amend ruff format command.

## [0.2.2] - 2025-02-13
### Changed
 - Add local dev command to port forward kubernetes pods.

## [0.2.3] - 2025-02-19
### Added
 - Add docker.pull as a convience and symmetry command to docker.push.
### Changed
 - Refactor entire repositories into modular composable components.

## [0.2.4] - 2025-03-05
### Changed
 - docker.configure now registers QEMU for multi-platform builds.

## [0.2.6] - 2025-03-05
### Changed
 - New command local.argo-submit to submit workflows from templates in argo.

## [0.2.8] - 2025-07-30
### Changed
 - Adding `serviceName` key to the local.ports configuration to port forward a service.

## [0.2.9] - 2025-07-31
### Changed
 - Fix local.ports -u option not unforwarding when using serviceName

## [0.2.10] - 2025-09-12
### Changed
 - Use `ruff format --check` instead of just `ruff format`

## [0.2.11] - 2025-10-29
### Changed
 - Add support to build & publish python packages via `uv`

## [0.3.0] - 2025-10-29
### Changed
 - Change CircleCI image to v3.12 instead of v3.12.8, droopping the patch version.
 - Migrate from Poetry to uv for package management.

## [0.4.0] - 2026-01-08
### Changed
 - Add kubeconform to helm.lint command
