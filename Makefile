# see https://makefiletutorial.com/

SHELL := /bin/bash -eu -o pipefail
PYTHON_3 ?= python3
PYTHON_D ?= $(HOME)/.python.d
SOURCE_PATHS := "src"

VENV_PATH_DEV := $(PYTHON_D)/dev/eclipse/xfsc/dev-ops/testing/bdd-executor/core
VENV_PATH_PROD := $(PYTHON_D)/prod/eclipse/xfsc/dev-ops/testing/bdd-executor/core

setup_dev: $(VENV_PATH_DEV)
	mkdir -p .tmp/

$(VENV_PATH_DEV):
	$(PYTHON_3) -m venv $(VENV_PATH_DEV)
	"$(VENV_PATH_DEV)/bin/pip" install -U pip wheel
	"$(VENV_PATH_DEV)/bin/pip" install -e ".[dev]"
	"$(VENV_PATH_DEV)/bin/pip" freeze > requirements-dev.txt


setup_prod: $(VENV_PATH_PROD)

$(VENV_PATH_PROD):
	$(PYTHON_3) -m venv $(VENV_PATH_PROD)
	"$(VENV_PATH_PROD)/bin/pip" install -U pip wheel
	"$(VENV_PATH_PROD)/bin/pip" install .
	"$(VENV_PATH_PROD)/bin/pip" freeze > requirements-prod.txt

isort: setup_dev
	"$(VENV_PATH_DEV)/bin/isort" $(SOURCE_PATHS) tests

pylint: setup_dev
	"$(VENV_PATH_DEV)/bin/pylint" $${ARG_PYLINT_JUNIT:-} $(SOURCE_PATHS) tests

coverage_run: setup_dev
	"$(VENV_PATH_DEV)/bin/coverage" run -m pytest $${ARG_COVERAGE_PYTEST:-} -m "not integration" tests/ src/

coverage_report: setup_dev
	"$(VENV_PATH_DEV)/bin/coverage" report

mypy: setup_dev
	"$(VENV_PATH_DEV)/bin/mypy" $${ARG_MYPY_SOURCE_XML:-} -p eu.xfsc.bdd.core

code_check: \
	setup_dev \
	isort \
	pylint \
	coverage_run coverage_report \
	mypy

run_coverage: coverage_run coverage_report

clean_dev:
	rm -rfv "$(VENV_PATH_DEV)"

clean_prod:
	rm -rfv "$(VENV_PATH_PROD)"

activate_env_prod:
	@echo "source \"$(VENV_PATH_PROD)/bin/activate\""

activate_env_dev:
	@echo "source \"$(VENV_PATH_DEV)/bin/activate\""

ansible:
	cd deployment/bare_metal && ansible-playbook main.ansible.yaml --connection=local -i localhost,
