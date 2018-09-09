SHELL=/bin/bash -e


gaia_test:
	cd tests
	pytest --cov=gaia --cov-report=term-missing

install:
	pip install -e ."[test, doc]"
