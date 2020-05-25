VENV_DIR=venv
SRC_DIR=src
PYTHON_CMD=python3

help:
	@echo "    setup             - Setup local dev environment"
	@echo "    test              - Run the tests"
	@echo "    format            - Format the codebase"
	@echo "    run               - Run streamkeeper"


setup:
	virtualenv ${VENV_DIR} -p ${PYTHON_CMD}
	${VENV_DIR}/bin/pip install -r requirements.txt -q

test:
	PYTHONPATH=${SRC_DIR} ${VENV_DIR}/bin/pytest

lint:
	${VENV_DIR}/bin/black

run:
	${VENV_DIR}/bin/python ${SRC_DIR}/streamkeeper.py