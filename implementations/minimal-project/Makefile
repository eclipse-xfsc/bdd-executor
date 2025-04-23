# see https://makefiletutorial.com/

SHELL := /bin/bash -eu -o pipefail
PYTHON_3 ?= python3
PYTHON_D ?= $(HOME)/.python.d
SOURCE_PATHS := "src"

VENV_PATH_DEV := $(PYTHON_D)/dev/eclipse/xfsc/dev-ops/testing/bdd-executor/minimal-project
VENV_PATH_PROD := $(PYTHON_D)/prod/eclipse/xfsc/dev-ops/testing/bdd-executor/minimal-project

DOCKER ?= docker
EU_XFSC_BDD_CORE_PATH ?= ../..


setup_dev: $(VENV_PATH_DEV)
	mkdir -p .tmp/

$(VENV_PATH_DEV):
	$(PYTHON_3) -m venv $(VENV_PATH_DEV)
	"$(VENV_PATH_DEV)/bin/pip" install -U pip wheel
	cd $(EU_XFSC_BDD_CORE_PATH) && "$(VENV_PATH_DEV)/bin/pip" install -e ".[dev]"
	"$(VENV_PATH_DEV)/bin/pip" install -e ".[dev]"

setup_prod: $(VENV_PATH_PROD)

$(VENV_PATH_PROD):
	$(PYTHON_3) -m venv $(VENV_PATH_PROD)
	"$(VENV_PATH_PROD)/bin/pip" install -U pip wheel
	cd $(EU_XFSC_BDD_CORE_PATH) && "$(VENV_PATH_PROD)/bin/pip" install "."
	"$(VENV_PATH_PROD)/bin/pip" install .

isort: setup_dev
	"$(VENV_PATH_DEV)/bin/isort" $(SOURCE_PATHS) tests

pylint: setup_dev
	"$(VENV_PATH_DEV)/bin/pylint" $${ARG_PYLINT_JUNIT:-} $(SOURCE_PATHS) tests

coverage_run: setup_dev
	"$(VENV_PATH_DEV)/bin/coverage" run -m pytest $${ARG_COVERAGE_PYTEST:-} -m "not integration" tests/ src/

coverage_report: setup_dev
	"$(VENV_PATH_DEV)/bin/coverage" report

mypy: setup_dev
	"$(VENV_PATH_DEV)/bin/mypy" $${ARG_MYPY_SOURCE_XML:-} $(SOURCE_PATHS)
	"$(VENV_PATH_DEV)/bin/mypy" $${ARG_MYPY_STEPS_XML:-} steps/ --disable-error-code=misc

code_check: \
	setup_dev \
	isort \
	pylint \
	coverage_run coverage_report \
	mypy

run_bdd_prod: setup_prod
	source "$(VENV_PATH_PROD)/bin/activate" && behave

run_bdd_dev: setup_dev
	source "$(VENV_PATH_DEV)/bin/activate" && \
		"$(VENV_PATH_DEV)/bin/coverage" run --append -m behave $${ARG_BDD_JUNIT:-} features/*

run_all_test_coverage: coverage_run run_bdd_dev coverage_report

clean_dev:
	rm -rfv  "$(VENV_PATH_DEV)"

clean_prod:
	rm -rfv  "$(VENV_PATH_PROD)"

activate_env_prod:
	@echo "source \"$(VENV_PATH_PROD)/bin/activate\""

activate_env_dev:
	@echo "source \"$(VENV_PATH_DEV)/bin/activate\""

ansible:
	cd deployment/bare_metal && ansible-playbook main.ansible.yaml --connection=local -i localhost,

download-selenium:
	wget --no-clobber \
          -P "./downloads/" \
          https://github.com/plantuml/plantuml/releases/download/v1.2023.13/plantuml-mit-1.2023.13.jar

docker-run-spring-boot-hello-world:
	$(DOCKER) run --rm -p 42511:8080 docker.io/avthart/spring-boot-hello-world
