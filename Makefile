help:
	@echo "    setup             - Setup local dev environment"
	@echo "    test              - Run the tests"
	@echo "    format            - Format the codebase"
	@echo "    start             - Start streamkeeper"
	@echo "    daemon            - Background streamkeeper"


setup:
	pip 
	@poetry install
	@poetry run pre-commit install 


test:
	@poetry run pytest tests/

.PHONY: format lint
format:
	@poetry run pre-commit run --all-files || \
		( echo "Pre-commit has the following changes:\n----------" && git --no-pager diff \
			&& echo "----------\n(Replace any starred output with the real values if you want to apply the patch)" \
			&& false )

start:
	@poetry run streamkeeper/streamkeeper.py process

daemon:
	@poetry run streamkeeper/streamkeeper.py daemon