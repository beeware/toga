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
