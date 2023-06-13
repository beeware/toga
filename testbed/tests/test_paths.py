import os
import shutil

import pytest


@pytest.mark.parametrize("attr", ["config", "data", "cache", "logs"])
async def test_app_paths(app, app_probe, attr):
    """Platform paths are as expected."""
    path = getattr(app.paths, attr)
    assert path == getattr(app_probe, f"{attr}_path")

    try:
        # We can create a folder in the app path
        tempdir = path / f"testbed-{os.getpid()}"
        tempdir.mkdir(parents=True)

        # We can create a file in the app path
        tempfile = tempdir / f"{attr}.txt"
        with tempfile.open("w", encoding="utf-8") as f:
            f.write(f"Hello {attr}\n")

        # We can create a file in the app path
        with tempfile.open("r", encoding="utf-8") as f:
            assert f.read() == f"Hello {attr}\n"

    finally:
        if path.exists():
            shutil.rmtree(tempdir)
