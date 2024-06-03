import pytest

import toga


def test_missing_widget():
    with pytest.raises(NotImplementedError):
        toga.platform.get_platform_factory().MissingWidget
