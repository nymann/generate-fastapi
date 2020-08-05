lint-dependencies:
	@pip install yapf pylint 'isort<5.0'

lint: lint-dependencies
	yapf --style google -dpr src
	pylint --rcfile=setup.cfg -r n src > pylint.txt
