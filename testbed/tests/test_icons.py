from importlib import import_module

import toga


def icon_probe(app, image):
    module = import_module("tests_backend.icons")
    return module.IconProbe(app, image)


async def test_icon(app):
    """An icon can be specified"""
    icon = toga.Icon("resources/icons/green")

    probe = icon_probe(app, icon)
    probe.assert_icon_content("resources/icons/green")

    # Create a second icon using an alternate (non-preferred) resource format.
    icon = toga.Icon(probe.alternate_resource)

    probe = icon_probe(app, icon)
    probe.assert_icon_content(probe.alternate_resource)


async def test_app_icon(app):
    """The app icon can be obtained."""
    probe = icon_probe(app, toga.Icon.APP_ICON)
    probe.assert_app_icon_content()


async def test_system_icon(app):
    """The default icon can be obtained"""
    probe = icon_probe(app, toga.Icon.DEFAULT_ICON)
    probe.assert_default_icon_content()


async def test_platform_icon(app):
    """A platform-specific icon can be loaded"""
    probe = icon_probe(app, toga.Icon("resources/logo"))
    probe.assert_platform_icon_content()


async def test_bad_icon_file(app):
    """If a file isn't a loadable icon, the default icon is used."""
    probe = icon_probe(app, toga.Icon("resources/icons/bad"))
    probe.assert_default_icon_content()
