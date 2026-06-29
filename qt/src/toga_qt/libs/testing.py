import os


def get_testing():  # pragma: no cover
    return bool(os.environ.get("PYTEST_VERSION"))
