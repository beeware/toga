import pytest

import toga


def test_importing_not_existent_gtk_submodule():
    with pytest.raises(NotImplementedError):
        toga.platform.get_platform_factory().notamodule
