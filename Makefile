# system python interpreter. used only to create virtual environment
NAME = l4logic
SCRIPT_NAME = l4logic
PY = python3
VENV = venv
BIN=$(VENV)/bin
BASH = $(shell which bash)
CWD = $(shell pwd)
GLOBAL_PATH = /usr/local/bin

PYTHON ?= $(shell \
	     (which python3) \
	     || (python -c 'import sys; sys.exit(sys.version < "2.6")' && \
	      which python) \
	     || (python2 -c 'import sys; sys.exit(sys.version < "2.6")' && \
	         which python2) \
	   )
ifeq ($(PYTHON),)
  $(error No suitable python found. Install minimum required from README)
endif

$(VENV): requirements.txt
	$(PY) -m venv $(VENV)
	$(BIN)/pip install --upgrade -r requirements.txt
	touch $(VENV)

.PHONY: test, install
install: $(VENV)
	echo '#!/usr/bin/bash' > $(SCRIPT_NAME)
	echo '#!$(PYTHON)' >> $(SCRIPT_NAME)
	echo '$(BIN)/python main.py' >> $(SCRIPT_NAME)
	chmod 777 $(SCRIPT_NAME)

install_globally:
	$(PYTHON) -m pip install --upgrade -r requirements.txt
	echo '#!/usr/bin/bash' > $(SCRIPT_NAME)
	echo '#!$(PYTHON)' >> $(SCRIPT_NAME)
	echo '$(PYTHON) $(CWD)/main.py' >> $(SCRIPT_NAME)
	chmod 777 $(SCRIPT_NAME)
	sudo cp ./$(SCRIPT_NAME) $(GLOBAL_PATH)

test: $(VENV)
	$(BIN)/$(PY) -m unittest discover tests

clean:
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete

uninstall:
	rm -rf $(VENV)
	find . -type f -name *.pyc -delete
	find . -type d -name __pycache__ -delete
	rm -f ./l4logic
	rm -f $(GLOBAL_PATH)/l4logic

help:
	@echo 'make install:             Install $(NAME) but locally with dependencies in virtual environement'
	@echo 'make install_globally:    Install $(NAME) globally'
	@echo 'make clean:               Remove the compiled files (*.pyc, *.pyo)'
	@echo 'make uninstall:           Remove the compiled files (*.pyc, *.pyo), virtual environement and executable file both from path and locally in CWD'
	@echo 'make test:                Test everything'
