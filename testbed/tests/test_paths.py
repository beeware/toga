import os
import shutil

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


def test_invalid_env_vars(app, monkeypatch):
    """If an environment variable is invalid (e.g. relative), it is ignored."""
    import sys

    if sys.platform == "darwin" or sys.platform == "ios":
        pytest.skip("macOS and iOS do not use environment variables for paths")

    monkeypatch.setenv("XDG_CONFIG_HOME", "relative/config")
    monkeypatch.setenv("LOCALAPPDATA", "relative/localappdata")

    # Clear cached _app_dir if it exists (win32 and textual-windows)
    app._impl.paths.__dict__.pop("_app_dir", None)

    # We call the backend implementation directly to avoid the cached
    # property on the core object
    config_path = app._impl.paths.get_config_path()

    # Assert it falls back to the default (absolute path within home dir)
    assert "relative" not in str(config_path)
    assert config_path.is_absolute()
