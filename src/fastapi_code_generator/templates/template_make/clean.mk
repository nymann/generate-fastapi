
clean: clean-${TARGET}

clean-docker:
	@docker-compose exec ${COMPONENT} make clean-local

clean-local:
	@git clean -n

clean-ci: clean-local

clean-production: clean-local
