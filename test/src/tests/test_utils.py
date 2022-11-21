# TODO: rename to utils.py once optimizations are disabled in the stub app. Until then,
# assertions in files not named test_*.py will raise "PytestConfigWarning: assertions not
# in test modules or plugins will be ignored".


def set_get(obj, name, value):
    """Calls a setter, then verifies that the same value is returned by the getter."""
    setattr(obj, name, value)
    assert getattr(obj, name) == value
