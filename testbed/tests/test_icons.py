import re
from importlib import import_module

import pytest

import toga


def icon_probe(app, image):
    module = import_module("tests_backend.icons")
    return getattr(module, "IconProbe")(app, image)


async def test_icon(app):
    "An icon can be specified"
    icon = toga.Icon("resources/icons/green")

    probe = icon_probe(app, icon)
    probe.assert_icon_content("resources/icons/green")

    # Create a second icon using an alternate (non-preferred) resource format.
    icon = toga.Icon(probe.alternate_resource)

    probe = icon_probe(app, icon)
    probe.assert_icon_content(probe.alternate_resource)


async def test_system_icon(app):
    "The default icon can be obtained"
    probe = icon_probe(app, toga.Icon.DEFAULT_ICON)
    probe.assert_default_icon_content()


async def test_bad_icon_file(app):
    "If a file isn't a loadable icon, an error is raised"
    with pytest.raises(
        ValueError,
        match=rf"Unable to load icon from {re.escape(str(app.paths.app / 'resources' / 'icons' / 'bad'))}",
    ):
        toga.Icon("resources/icons/bad")
