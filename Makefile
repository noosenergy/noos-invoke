SHELL := /bin/sh -e

.DEFAULT_GOAL := help


# Helper
.PHONY: help

help:  ## Display this auto-generated help message
	@grep -E '^[0-9a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
	awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'


# Development
.PHONY: update clean format

update:  ## Lock and install build dependencies
	poetry update

clean:  ## Clean project from temp files / dirs
	rm -rf build dist
	find src -type d -name __pycache__ | xargs rm -rf

format:  ## Run auto-formatting linters
	poetry run ruff check --select I --fix src
	poetry run ruff format src


# Deployment
.PHONY: install lint test package release

install:  ## Install build dependencies from lock file
	poetry install

lint:  ## Run python linters
	poetry run ruff check src
	poetry run mypy src

test:  ## Run pytest with all tests
	poetry run pytest src/tests

package:  ## Build project wheel distribution
	poetry build

release:  ## Publish wheel distribution to PyPi
	poetry publish --build -u ${PYPI_USER} -p ${PYPI_TOKEN}
