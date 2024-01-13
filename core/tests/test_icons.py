from pathlib import Path

import pytest

import toga
import toga_dummy
from toga_dummy.icons import Icon as DummyIcon

APP_RESOURCES = Path(__file__).parent / "resources"
TOGA_RESOURCES = Path(toga_dummy.__file__).parent / "resources"


class MyApp(toga.App):
    pass


@pytest.fixture
def app():
    return MyApp("Icons Test", "org.beeware.toga.icons")


@pytest.mark.parametrize(
    "path, system, sizes, extensions, final_paths",
    [
        # Relative path
        (Path("resources/red"), False, None, [".png"], APP_RESOURCES / "red.png"),
        # Absolute path (points at a file in the system resource folder,
        # but that's just because it's a location we know exists.)
        (
            TOGA_RESOURCES / "toga",
            False,
            None,
            [".png"],
            TOGA_RESOURCES / "toga.png",
        ),
        # PNG format
        ("resources/red", False, None, [".png"], APP_RESOURCES / "red.png"),
        # Explicitly specified as BMP, but ignored because platform wants PNG format
        ("resources/red.bmp", False, None, [".png"], APP_RESOURCES / "red.png"),
        # PNG format in multiple sizes
        (
            "resources/red",
            False,
            [32, 72],
            [".png"],
            {
                32: APP_RESOURCES / "red-32.png",
                72: APP_RESOURCES / "red-72.png",
            },
        ),
        # PNG format in multiple sizes, but no individually sized PNGs available
        (
            "resources/blue",
            False,
            [32, 72],
            [".png"],
            {
                32: APP_RESOURCES / "blue.png",
                72: APP_RESOURCES / "blue.png",
            },
        ),
        # Multiple formats, first option doesn't exist
        ("resources/blue", False, None, [".bmp", ".png"], APP_RESOURCES / "blue.png"),
        # Multiple formats, first match returned
        (
            "resources/orange",
            False,
            None,
            [".bmp", ".png"],
            APP_RESOURCES / "orange.bmp",
        ),
        # Relative path, platform-specific resource
        (
            Path("resources/sample"),
            False,
            None,
            [".png"],
            APP_RESOURCES / "sample-dummy.png",
        ),
        # Relative path as string, platform-specific resource
        (
            "resources/sample",
            False,
            None,
            [".png"],
            APP_RESOURCES / "sample-dummy.png",
        ),
        # Relative path, system resource
        (Path("toga"), True, None, [".png"], TOGA_RESOURCES / "toga.png"),
        # Relative path as string, system resource
        ("toga", True, None, [".png"], TOGA_RESOURCES / "toga.png"),
    ],
)
def test_create(monkeypatch, app, path, system, sizes, extensions, final_paths):
    "Icons can be created"
    # Patch the dummy Icon class to evaluated different lookup strategies.
    monkeypatch.setattr(DummyIcon, "SIZES", sizes)
    monkeypatch.setattr(DummyIcon, "EXTENSIONS", extensions)

    # monkeypatch the current platform to report as dummy
    monkeypatch.setattr(toga.platform, "current_platform", "dummy")

    icon = toga.Icon(path, system=system)

    # Icon is bound
    assert icon._impl is not None
    # impl/interface round trips
    assert icon._impl.interface == icon

    # The icon's path is fully qualified
    assert icon._impl.path == final_paths


def test_create_fallback(app):
    "If a resource doesn't exist, a fallback icon is used."
    icon = toga.Icon("resources/missing")

    assert icon._impl is not None
    assert icon._impl.interface == toga.Icon.DEFAULT_ICON


@pytest.mark.parametrize(
    "name, path",
    [
        ("DEFAULT_ICON", "toga"),
        ("OPTION_CONTAINER_DEFAULT_TAB_ICON", "optioncontainer-tab"),
    ],
)
def test_cached_icons(app, name, path):
    "Default icons exist, and are cached"

    icon = getattr(toga.Icon, name)
    assert icon.path == Path(path)

    # Retrieve the icon a second time; The same instance is returned.
    assert id(getattr(toga.Icon, name)) == id(icon)


def test_deprecated_icons(app):
    """Deprecated icons are still available"""
    with pytest.warns(DeprecationWarning):
        icon = toga.Icon.TOGA_ICON
    assert icon.path == Path("toga")

    # Retrieve the icon a second time; The same instance is returned.
    assert id(toga.Icon.TOGA_ICON) == id(icon)
