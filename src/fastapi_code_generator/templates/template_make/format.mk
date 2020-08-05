format: format-${TARGET}

format-local:
	@isort --recursive src
	@yapf --style google -ipr src
	@pylint --rcfile=setup.cfg src

format-docker: install-docker
	@docker-compose exec ${COMPONENT} make TARGET=local format

format-ci:
	@echo "WRONG USAGE: Don't use format as part of CI."
	exit 2

format-production:
	@echo "WRONG USAGE: Don't format code in production."
	exit 2
