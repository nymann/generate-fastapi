test: test-${TARGET}

test-docker: ${VERSION} requirements.install
	${SCRIPTS_DIR}/docker_test.sh

test-local: ${VERSION} requirements.install
	@python setup.py test

test-ci: test-docker

test-production:
