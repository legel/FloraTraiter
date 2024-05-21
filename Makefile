.PHONY: test install dev venv clean activate base
.ONESHELL:

VENV=.venv
PY_VER=python3.11
PYTHON=$(VENV)/bin/python
PIP_INSTALL=$(PYTHON) -m pip install
SPACY_MODEL=$(PYTHON) -m spacy download en_core_web_md

test: activate
	export MOCK_TRAITER=1
	$(PYTHON) -m unittest discover
	export MOCK_TRAITER=0

install: venv base
	$(PIP_INSTALL) git+https://github.com/rafelafrance/common_utils.git@main#egg=common_utils
	$(PIP_INSTALL) git+https://github.com/rafelafrance/spell-well.git@main#egg=spell-well
	$(PIP_INSTALL) git+https://github.com/rafelafrance/traiter.git@master#egg=traiter
	$(PIP_INSTALL) .
	$(SPACY_MODEL)

dev: venv base
	$(PIP_INSTALL) -e ../../misc/common_utils
	$(PIP_INSTALL) -e ../../misc/spell-well
	$(PIP_INSTALL) -e ../../traiter/traiter
	$(PIP_INSTALL) -e .[dev]
	$(SPACY_MODEL)
	pre-commit install

activate:
	test -d $(VENV) || $(PY_VER) -m venv $(VENV)
	. $(VENV)/bin/activate

base:
	if [ ! -f $(VENV)/bin/pip ]; then \
	    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py; \
	    $(PYTHON) get-pip.py; \
	    rm get-pip.py; \
	fi
	$(PIP_INSTALL) -U pip setuptools wheel

venv:
	test -d $(VENV) || $(PY_VER) -m venv $(VENV)

clean:
	rm -rf $(VENV)
	find -iname "*.pyc" -delete

