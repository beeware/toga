import pytest

from toga import Command


async def test_unknown_system_command(app):
    """Attempting to create an unknown standard command raises an error."""
    with pytest.raises(ValueError, match=r"Unknown standard command 'mystery'"):
        Command.standard(app, "mystery")
