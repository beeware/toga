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


@pytest.mark.parametrize("attr", ["documents", "pictures", "desktop"])
async def test_user_paths(app, app_probe, attr):
    """User paths are platform-appropriate and cached."""
    if hasattr(app_probe, f"{attr}_path"):
        path = getattr(app.paths, attr)
        assert path == getattr(app_probe, f"{attr}_path")
        assert path.exists()
        assert getattr(app.paths, attr) == path
    else:
        with pytest.raises(RuntimeError) as exc_info:
            getattr(app.paths, attr)
        assert type(exc_info.value) is RuntimeError
