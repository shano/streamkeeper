VENV_DIR=venv
SRC_DIR=src
PYTHON_CMD=python3

help:
	@echo "    setup             - Setup local dev environment"
	@echo "    test              - Run the tests"
	@echo "    format            - Format the codebase"
	@echo "    run               - Run streamkeeper"


setup:
	${PYTHON_CMD} -m venv ${VENV_DIR}
	${VENV_DIR}/bin/pip install -r requirements.txt -q
	${VENV_DIR}/bin/pip install -r requirements-dev.txt -q

test:
	PYTHONPATH=${SRC_DIR} ${VENV_DIR}/bin/pytest

lint:
	${VENV_DIR}/bin/black ${SRC_DIR}

start:
	${VENV_DIR}/bin/python ${SRC_DIR}/streamkeeper.py process

daemon:
	${VENV_DIR}/bin/python ${SRC_DIR}/streamkeeper.py daemon