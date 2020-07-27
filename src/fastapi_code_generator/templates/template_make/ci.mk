CI_REGISTRY_IMAGE?=mo-gitlab.siemens.dk:4567/sw-group/banedanmark/s-bane/pykpi/tlog/components/frontend
ONBUILD?=${CI_REGISTRY_IMAGE}:onbuild
ONBUILD_VER?=${ONBUILD}

docker-build-onbuild-ci: ${VERSION} requirements.install
	@docker build -f docker/Dockerfile .

docker-push-onbuild-ci: ${VERSION} requirements.install
	@docker build --cache-from ${ONBUILD} -t ${ONBUILD} -t ${ONBUILD_VER} -f docker/Dockerfile .
	@docker push ${CI_REGISTRY_IMAGE}

.PHONY:docker-build-onbuild-ci docker-push-onbuild-ci
