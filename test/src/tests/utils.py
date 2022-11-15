def set_get(obj, name, value):
    """Calls a setter, then verifies that the same value is returned by the getter."""
    setattr(obj, name, value)
    assert getattr(obj, name) == value
