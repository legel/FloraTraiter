.PHONY: test install dev venv clean
.ONESHELL:

VENV=.venv
PY_VER=python3.11
PYTHON=./$(VENV)/bin/$(PY_VER)
PIP_INSTALL=$(PYTHON) -m pip install
SPACY_MODEL=$(PYTHON) -m spacy download en_core_web_md
ACTIVATE=. $(VENV)/bin/activate

test:
	$(ACTIVATE)
	export MOCK_DATA=1
	$(PYTHON) -m unittest discover
	export MOCK_DATA=0

install: venv
	$(ACTIVATE)
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) git+https://github.com/rafelafrance/common_utils.git@main#egg=common_utils
	$(PIP_INSTALL) git+https://github.com/rafelafrance/spell-well.git@main#egg=spell-well
	$(PIP_INSTALL) git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
	$(PIP_INSTALL) .
	$(SPACY_MODEL)

dev: venv
	$(ACTIVATE)
	$(PIP_INSTALL) -U pip setuptools wheel
	$(PIP_INSTALL) -e ../../misc/common_utils
	$(PIP_INSTALL) -e ../../misc/spell-well
	$(PIP_INSTALL) -e ../../traiter/traiter
	$(PIP_INSTALL) -e .[dev]
	$(SPACY_MODEL)
	pre-commit install

venv:
	test -d $(VENV) || $(PY_VER) -m venv $(VENV)

clean:
	rm -r $(VENV)
	find -iname "*.pyc" -delete
