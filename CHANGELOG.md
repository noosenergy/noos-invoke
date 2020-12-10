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
