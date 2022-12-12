import os
import sys
import tempfile
from functools import partial
from pathlib import Path
from threading import Thread

import coverage
import pytest

from testbed.app import main


def run_tests(app):
    project_path = Path(__file__).parent.parent
    os.chdir(project_path)

    # TODO: replace with extractPackages.
    if hasattr(sys, "getandroidapilevel"):
        import tests

        chaquopy_extract_package(tests)

    pytest.main(
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
    # Determine the toga backend. This replicates the behavior in toga/platform.py;
    # we can't use that module directly because we need to capture all the import
    # side effects as part of the coverage data.
    try:
        toga_backend = os.environ["TOGA_BACKEND"]
    except KeyError:
        if hasattr(sys, "getandroidapilevel"):
            toga_backend = "toga_android"
        else:
            toga_backend = {
                "darwin": "toga_cocoa",
                "ios": "toga_iOS",
                "linux": "toga_gtk",
                "emscripten": "toga_web",
                "win32": "toga_winforms",
            }.get(sys.platform)

    # Start coverage tracking
    cov = coverage.Coverage(
        # Don't store any coverage data
        data_file=None,
        source_pkgs=[toga_backend],
    )
    cov.start()

    # Create the test app, starting the test suite as a background task
    app = main()
    thread = Thread(target=partial(run_tests, app))
    app.add_background_task(lambda app, *kwargs: thread.start())

    # Install an on-exit handler that will output the coverage report
    def report_coverage(app, **kwargs):
        cov.stop()

        # FIXME: Coverage reporting doesn't work on Android (yet!)
        # Output an answer that will get picked up by the exit pattern.
        if hasattr(sys, "getandroidapilevel"):
            print("***No coverage report on Android***")
            print()
            print("0 files skipped due to complete coverage.")
            return True

        cov.report(
            precision=1,
            skip_covered=True,
            show_missing=True,
        )
        return True

    app.on_exit = report_coverage

    # Start the test app.
    app.main_loop()
