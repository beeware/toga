import pytest


async def test_raise_not_implemented_error_on_unsupported_widget(app):
    with pytest.raises(NotImplementedError) as exc:
        _ = app.factory.nothing
    assert "Toga's Dummy backend doesn't implement nothing" in str(exc)
