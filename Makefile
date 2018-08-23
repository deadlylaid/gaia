SHELL=/bin/bash -e


test:
	pytest --cov=gaia --cov-report=term-missing

install:
	pip install -e ."[test, doc]"
