include subtrees/z_quantum_actions/Makefile


coverage:
	qvm -S &
	quilc -S &
	$(PYTHON) -m pytest -m "not integration" \
		--cov=src \
		--cov-fail-under=$(MIN_COVERAGE) tests \
		--no-cov-on-fail \
		--cov-report xml \
		&& echo Code coverage Passed the $(MIN_COVERAGE)% mark!

github_actions-default:
	apt-get update
	apt-get install -y python3.7-venv
	python3 -m venv ${VENV} && \
		${VENV}/bin/python3 -m pip install --upgrade pip && \
		${VENV}/bin/python3 -m pip install ./z-quantum-core && \
		${VENV}/bin/python3 -m pip install -e '.[develop]'

mypy-default: clean
	@echo scanning files with mypy: Please be patient....
	$(PYTHON) -m pip show numpy
	$(PYTHON) -m pip show mypy
	$(PYTHON) -m mypy src tests