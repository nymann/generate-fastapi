
.PHONY: install hooks lint install test fix clean help

PLATFORM?=local
TMP_HOOKS:=/tmp/.generate_fastapi_hooks_empty.target
VERSION:=src/generate_fastapi/version.py

.DEFAULT:help
help:
	@printf "The following commands are available:\n\n"
	@printf "\e[92m%s\e[0m\n" "make hooks"
	@echo " - setup pre-commit hooks"
	@printf "\e[92m%s\e[0m\n" "make test"
	@echo " - run tests"
	@printf "\e[92m%s\e[0m\n" "make lint"
	@echo " - Autoformats code and sorts imports (unless running as 'ci')."
	@printf "\e[92m%s\e[0m\n" "make run"
	@echo " - runs generate_fastapi"

${VERSION}:
	@echo "__version__ = \"$(shell git describe --tag --always | grep -oE '[0-9]+\.[0-9]+\.[0-9]+')\"" > ${VERSION}

hooks:${TMP_HOOKS}
${TMP_HOOKS}:.pre-commit-config.yaml
	@pip install pre-commit > /dev/null
	@pre-commit install > /dev/null
	@pre-commit run --all-files || \
		(printf "\e[93m%s\e[0m\n" "Run same make target again";exit 1)
	@printf "\e[92m%s\e[0m\n" "Pre-commit hooks ran successfully"
	@touch /tmp/.generate_fastapi_hooks_empty_target

lint:
	@pip install wemake-python-styleguide
	@git diff -u | flake8 --diff src --exclude='src/generate_fastapi/mako_templates/**/*.py'

install: ${VERSION}
	@python3 setup.py develop

deploy: ${VERSION}
	@python3 -m pip install --upgrade pip
	@pip install setuptools wheel twine
	@python3 setup.py sdist bdist_wheel
	@twine upload dist/*

test: install
	@python3 setup.py test

fix: hooks
	@isort --recursive src tests -sg="**/mako_templates/**/*.py"
	@autopep8 -ir src tests --exclude='src/generate_fastapi/mako_templates/**/*.py'
clean:
	@find src tests | grep -E "(__pycache__|\.pyc)" | xargs rm -rf
	@rm -rf \
		src/generate_fastapi.egg-info/ \
		.eggs/ \
		.coverage \
		htmlcov/ \
		dist/ \
		build/ \
		coverage.xml \
		pylint.txt
