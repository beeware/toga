from pathlib import Path

import pytest

import toga
from toga_dummy.icons import Icon as DummyIcon

APP_RESOURCES = Path(__file__).parent / "resources"
TOGA_RESOURCES = Path(toga.__file__).parent / "resources"


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
            Path(__file__).parent.parent / "src" / "toga" / "resources" / "toga",
            False,
            None,
            [".png"],
            Path(__file__).parent.parent / "src" / "toga" / "resources" / "toga.png",
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
        # Relative path, system resource
        (Path("resources/toga"), True, None, [".png"], TOGA_RESOURCES / "toga.png"),
        # Relative path as string, system resource
        (Path("resources/toga"), True, None, [".png"], TOGA_RESOURCES / "toga.png"),
    ],
)
def test_create(monkeypatch, app, path, system, sizes, extensions, final_paths):
    "Icons can be created"
    # Patch the dummy Icon class to evaluated different lookup strategies.
    monkeypatch.setattr(DummyIcon, "SIZES", sizes)
    monkeypatch.setattr(DummyIcon, "EXTENSIONS", extensions)

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
        ("DEFAULT_ICON", "resources/toga"),
        ("TOGA_ICON", "resources/toga"),
    ],
)
def test_cached_icons(app, name, path):
    "Default icons exist, and are cached"

    icon = getattr(toga.Icon, name)
    assert icon.path == Path("resources/toga")

    # Retrieve the icon a second time; The same instance is returned.
    assert id(getattr(toga.Icon, name)) == id(icon)
