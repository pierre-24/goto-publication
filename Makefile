all: help

help:
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  init                        to install python dependencies"
	@echo "  sync                        update dependencies of pipenv"
	@echo "  lint                        to lint backend code (flake8)"
	@echo "  test                        to run tests"
	@echo "  help                        to get this help"

install:
	pip install -e .
	pip3 install goto-publication[dev]

init: install
	python -c 'import nltk; nltk.download("wordnet")'  # used by iso4

sync:
	pip-sync

lint:
	flake8 goto_publication --max-line-length=120 --ignore=N802

tests:
	python -m unittest discover -s goto_publication.tests

