HOOKS            := hooks
INSTALL          := install
COVERAGE         := coverage
ETL              := etl
ETL_SRC          := $(wildcard $(ETL)/*)
COVER            := $(ETL_SRC:$(ETL)/%=$(COVERAGE)-$(ETL)-%)
MUSTPASS         := $(HOOKS) $(COVERAGE)

$(HOOKS): ## Run pre-commit hooks
	pre-commit run --all-files

format: isort black ## Format code with respect to all linters

black: ## Format code according to black
	black .

isort: ## Format imports according to isort
	isort .

clean: ## Remove previous coverage data
	find . -type f -name '*pyc' -exec rm -rf {} \;
	find . -type d -name '__pycache__' -prune -exec rm -rf {} \;
	$(COVERAGE) combine || true
	$(COVERAGE) erase

$(COVERAGE)-%:
	$(COVERAGE) run --source=$(subst -,/,$*) -p -m pytest -svv $(subst -,/,$*)  || true

$(COVERAGE): clean $(COVER) ## Run all code coverage commands, combine them, and report on results
	$(COVERAGE) combine
	$(COVERAGE) report --fail-under=100 --show-missing --ignore-errors $$(find $(ETL) -type f -name '*.py')

$(INSTALL):
	pip install -r requirements.txt
	pre-commit install

$(SETUP):
	python ddl/src/

test-build: $(MUSTPASS)