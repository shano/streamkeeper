help:
	@echo "    setup             - Setup local dev environment"
	@echo "    build             - Build project locally"
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

build:
	@poetry build

publish:
	@poetry publish

start:
	@poetry run streamkeeper process ./config.ini

daemon:
	@poetry run streamkeeper daemon ./config.ini