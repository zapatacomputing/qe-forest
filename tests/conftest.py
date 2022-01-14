import pytest

from qeforest.simulator import kill_subprocesses


def pytest_sessionfinish(session, exitstatus):
    kill_subprocesses()


def pytest_runtestloop(session):
    session.add_marker(
        pytest.mark.filterwarnings("ignore:Port 5000 which is used to run QVM")
    )
    session.add_marker(
        pytest.mark.filterwarnings("ignore:Port 5555 which is used to run QUILC")
    )
