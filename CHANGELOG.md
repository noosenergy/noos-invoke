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
