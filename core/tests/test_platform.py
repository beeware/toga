import sys
from unittest.mock import Mock

import pytest

import toga_dummy

if sys.version_info >= (3, 10):
    from importlib.metadata import EntryPoint
else:
    # Before Python 3.10, entry_points did not support the group argument;
    # so, the backport package must be used on older versions.
    from importlib_metadata import EntryPoint

import toga.platform
from toga.platform import current_platform, get_current_platform, get_platform_factory


@pytest.fixture
def clean_env(monkeypatch):
    monkeypatch.delenv("TOGA_BACKEND")


@pytest.fixture
def platform_factory_1():
    return Mock()


@pytest.fixture
def platform_factory_2():
    return Mock()


def patch_platforms(monkeypatch, platforms):
    monkeypatch.setattr(
        sys,
        "modules",
        {f"{name}_module.factory": factory for name, factory, _ in platforms},
    )

    monkeypatch.setattr(
        toga.platform,
        "entry_points",
        Mock(
            return_value=[
                EntryPoint(
                    name=current_platform if is_current else name,
                    value=f"{name}_module",
                    group="self.backends",
                )
                for name, _, is_current in platforms
            ]
        ),
    )


def test_get_current_platform_desktop():
    assert (
        get_current_platform()
        == {
            "darwin": "macOS",
            "linux": "linux",
            "win32": "windows",
        }[sys.platform]
    )


def test_get_current_platform_android_inferred(monkeypatch):
    """Android platform can be inferred from existence of sys.getandroidapilevel."""
    monkeypatch.setattr(sys, "platform", "linux")
    try:
        # since there isn't an existing attribute of this name, it can't be patched.
        sys.getandroidapilevel = Mock(return_value=42)
        assert get_current_platform() == "android"
    finally:
        del sys.getandroidapilevel


def test_get_current_platform_android(monkeypatch):
    """Android platform can be obtained directly from sys.platform."""
    monkeypatch.setattr(sys, "platform", "android")
    try:
        # since there isn't an existing attribute of this name, it can't be patched.
        sys.getandroidapilevel = Mock(return_value=42)
        assert get_current_platform() == "android"
    finally:
        del sys.getandroidapilevel


def test_get_current_platform_iOS(monkeypatch):
    """IOS platform can be obtained directly from sys.platform."""
    monkeypatch.setattr(sys, "platform", "ios")
    assert get_current_platform() == "iOS"


def test_get_current_platform_web(monkeypatch):
    """Web platform can be obtained directly from sys.platform."""
    monkeypatch.setattr(sys, "platform", "emscripten")
    assert get_current_platform() == "web"


@pytest.mark.parametrize("value", ["freebsd12", "freebsd13", "freebsd14"])
def test_get_current_platform_freebsd(monkeypatch, value):
    """FreeBSD platform can be obtained directly from sys.platform."""
    monkeypatch.setattr(sys, "platform", value)
    assert get_current_platform() == "freeBSD"


def _get_platform_factory():
    get_platform_factory.cache_clear()
    factory = get_platform_factory()
    get_platform_factory.cache_clear()
    return factory


def test_no_platforms(monkeypatch, clean_env):
    patch_platforms(monkeypatch, [])
    with pytest.raises(
        RuntimeError,
        match=r"No Toga backend could be loaded.",
    ):
        _get_platform_factory()


def test_one_platform_installed(monkeypatch, clean_env):
    only_platform_factory = Mock()
    patch_platforms(monkeypatch, [("only_platform", only_platform_factory, False)])

    factory = _get_platform_factory()
    assert factory == only_platform_factory


def test_multiple_platforms_installed(monkeypatch, clean_env):
    current_platform_factory = Mock()
    other_platform_factory = Mock()
    patch_platforms(
        monkeypatch,
        [
            ("other_platform", other_platform_factory, False),
            ("current_platform", current_platform_factory, True),
        ],
    )

    factory = _get_platform_factory()
    assert factory == current_platform_factory


def test_multiple_platforms_installed_fail_both_appropriate(monkeypatch, clean_env):
    current_platform_factory_1 = Mock()
    current_platform_factory_2 = Mock()
    patch_platforms(
        monkeypatch,
        [
            ("current_platform_1", current_platform_factory_1, True),
            ("current_platform_2", current_platform_factory_2, True),
        ],
    )

    with pytest.raises(
        RuntimeError,
        match=(
            r"Multiple candidate toga backends found: \('current_platform_1_module' "
            r"\(.*\), 'current_platform_2_module' \(.*\)\). Uninstall the backends you "
            r"don't require, or use TOGA_BACKEND to specify a backend."
        ),
    ):
        _get_platform_factory()


def test_multiple_platforms_installed_fail_none_appropriate(monkeypatch, clean_env):
    other_platform_factory_1 = Mock()
    other_platform_factory_2 = Mock()
    patch_platforms(
        monkeypatch,
        [
            ("other_platform_1", other_platform_factory_1, False),
            ("other_platform_2", other_platform_factory_2, False),
        ],
    )

    with pytest.raises(
        RuntimeError,
        match=(
            r"Multiple Toga backends are installed \('other_platform_1_module' "
            r"\(.*\), 'other_platform_2_module' \(.*\)\), but none of them match "
            r"your current platform \('.*'\). Install a backend for your current "
            r"platform, or use TOGA_BACKEND to specify a backend."
        ),
    ):
        _get_platform_factory()


def test_environment_variable(monkeypatch):
    monkeypatch.setenv("TOGA_BACKEND", "toga_dummy")
    assert toga_dummy.factory == _get_platform_factory()


def test_environment_variable_fail(monkeypatch):
    monkeypatch.setenv("TOGA_BACKEND", "fake_platform_module")
    with pytest.raises(
        RuntimeError,
        match=r"The backend specified by TOGA_BACKEND \('fake_platform_module'\) could not be loaded.",
    ):
        _get_platform_factory()
