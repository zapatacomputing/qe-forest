include subtrees/z_quantum_actions/Makefile


PYTHON := $(shell which python3)

coverage:
	qvm -S &
	quilc -S &
	$(PYTHON) -m pytest -m "not integration" \
		--cov=src \
		--cov-fail-under=$(MIN_COVERAGE) tests \
		--no-cov-on-fail \
		--cov-report term-missing \
		&& echo Code coverage Passed the $(MIN_COVERAGE)% mark!
