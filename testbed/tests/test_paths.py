import os
import shutil
import tempfile
from pathlib import Path

import pytest


@pytest.mark.parametrize("attr", ["config", "data", "cache", "logs"])
async def test_app_paths(app, app_probe, attr):
    """Platform paths are as expected."""
    # Create path and confirm it exists
    path = getattr(app.paths, attr)
    assert path == getattr(app_probe, f"{attr}_path")

    try:
        # We can create a file in the app path
        tempfile = path / f"{attr}-{os.getpid()}.txt"

        # We can write to a file in the app path
        with tempfile.open("w", encoding="utf-8") as f:
            f.write(f"Hello {attr}\n")

        # We can read a file in the app path
        with tempfile.open("r", encoding="utf-8") as f:
            assert f.read() == f"Hello {attr}\n"

        # Attempt to create the path again to confirm it is the same
        newpath = getattr(app.paths, attr)
        assert newpath == path

    finally:
        try:
            if path.exists():
                shutil.rmtree(path)
        except PermissionError:
            pass


@pytest.mark.parametrize("attr", ["desktop", "documents", "downloads", "pictures"])
async def test_user_space_paths(app, app_probe, attr):
    """User-space folder paths are as expected."""
    expected = getattr(app_probe, f"{attr}_path")
    if expected is None:
        # The platform doesn't have user-space folders, so accessing the
        # path raises an error.
        with pytest.raises(RuntimeError):
            getattr(app.paths, attr)
        pytest.xfail(f"This platform does not have a {attr} folder")

    # These are the user's own folders; Toga will not create them, and this
    # test must not delete them. If a folder doesn't exist on this machine
    # (e.g., a minimal CI environment), create it for the duration of the
    # test, and remove it (without removing any content) afterwards.
    created = not expected.exists()
    if created:
        expected.mkdir(parents=True)

    try:
        path = getattr(app.paths, attr)
        assert path == expected
        assert path.exists()
    finally:
        if created:
            expected.rmdir()


async def test_xdg_user_dir_resolution(app_probe, monkeypatch):
    """User-space folder locations honor the xdg-user-dirs configuration."""
    if not app_probe.supports_xdg_user_dirs:
        pytest.skip("This backend doesn't resolve folders using xdg-user-dirs")

    # The tmp_path fixture can't be used here, as it can't be constructed on
    # the platforms that skip this test.
    with tempfile.TemporaryDirectory() as config_home_str:
        config_home = Path(config_home_str)
        monkeypatch.setenv("XDG_CONFIG_HOME", str(config_home))

        # With no configuration file, an explicitly set environment variable
        # is used.
        monkeypatch.setenv("XDG_DOCUMENTS_DIR", str(config_home / "env-documents"))
        assert app_probe.resolve_xdg_user_dir("XDG_DOCUMENTS_DIR", "Documents") == (
            config_home / "env-documents"
        )

        # With no configuration file and no environment variable, the default
        # folder name in the user's home folder is used.
        monkeypatch.delenv("XDG_DESKTOP_DIR", raising=False)
        assert app_probe.resolve_xdg_user_dir("XDG_DESKTOP_DIR", "Desktop") == (
            Path.home() / "Desktop"
        )

        # Entries in the configuration file are used, with $HOME expanded.
        (config_home / "user-dirs.dirs").write_text(
            'XDG_PICTURES_DIR="$HOME/My Pictures"\n'
        )
        assert app_probe.resolve_xdg_user_dir("XDG_PICTURES_DIR", "Pictures") == (
            Path.home() / "My Pictures"
        )

        # Keys missing from the configuration file fall back.
        monkeypatch.delenv("XDG_DOWNLOAD_DIR", raising=False)
        assert app_probe.resolve_xdg_user_dir("XDG_DOWNLOAD_DIR", "Downloads") == (
            Path.home() / "Downloads"
        )
