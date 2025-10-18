import os


def get_testing():
    return bool(os.environ.get("PYTEST_VERSION"))
