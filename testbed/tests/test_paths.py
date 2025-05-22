import os
import shutil

import pytest


@pytest.mark.parametrize("attr", ["config", "data", "cache", "logs"])
async def test_app_paths(app, app_probe, attr):
    with app_probe.prepare_paths() as expected_paths:
        """Platform paths are as expected."""
        path = getattr(app.paths, attr)
        assert path == expected_paths[attr]

        try:
            # We can create a folder in the app path
            tempdir = path / f"testbed-{os.getpid()}"
            tempdir.mkdir()  # Don't create parent, to confirm it already exists

            # We can create and write to a file in the app path
            tempfile = path / f"{attr}-{os.getpid()}.txt"
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
