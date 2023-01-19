import os
import sys
import tempfile
from functools import partial
from pathlib import Path
from threading import Thread

import pytest

from testbed.app import main


def run_tests(app):
    project_path = Path(__file__).parent.parent
    os.chdir(project_path)

    # TODO: replace with extractPackages.
    if hasattr(sys, "getandroidapilevel"):
        import tests

        chaquopy_extract_package(tests)

    app.returncode = pytest.main(
        [
            # Output formatting
            "-vv",
            "--no-header",
            "--tb=native",
            "-rP",  # Show stdout from all tests, even if they passed.
            "--color=no",
            # Run all async tests and fixtures using pytest-asyncio.
            "--asyncio-mode=auto",
            # Override the cache directory to be somewhere known writable
            "-o",
            f"cache_dir={tempfile.gettempdir()}/.pytest_cache",
            project_path / "tests",
        ]
    )
    app.add_background_task(lambda app, **kwargs: app.exit())


def chaquopy_extract_package(pkg):
    finder = pkg.__loader__.finder
    for path in pkg.__path__:
        chaquopy_extract_dir(finder, finder.zip_path(path))


def chaquopy_extract_dir(finder, zip_dir):
    for filename in finder.listdir(zip_dir):
        zip_path = f"{zip_dir}/{filename}"
        if finder.isdir(zip_path):
            chaquopy_extract_dir(finder, zip_path)
        else:
            finder.extract_if_changed(zip_path)


if __name__ == "__main__":
    app = main()
    thread = Thread(target=partial(run_tests, app))
    app.add_background_task(lambda app, *kwargs: thread.start())

    # Add an on_exit handler that will terminate the test suite.
    def exit_suite(app, **kwargs):
        print(f">>>>>>>>>> EXIT {app.returncode} <<<<<<<<<<")
        return True

    app.on_exit = exit_suite

    app.main_loop()
