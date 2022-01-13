from qeforest.simulator import kill_subprocesses


def pytest_sessionfinish(session, exitstatus):
    kill_subprocesses()
