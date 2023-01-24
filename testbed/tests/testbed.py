import os
import tempfile
from functools import partial
from pathlib import Path
from threading import Thread

import coverage
import pytest

from testbed.app import main


def run_tests(app, cov):
    project_path = Path(__file__).parent.parent
    os.chdir(project_path)
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

    # FIXME: Coverage reporting doesn't work on Android & iOS (yet!) This is for
    # two reasons:
    # 1. On Android, the code being covered needs to be unpacked and readable
    #    for a coverage report to be generated. This should be fixed by
    #    extractPackages
    # 2. The main thread where coverage has been started dies before the this
    #    thread; as a result, the garbage collection on the tracer function
    #    (coverage.pytracer._trace():132) raises an IndexError because the data
    #    stack is empty.
    if hasattr(sys, "getandroidapilevel"):
        print("***No coverage report on Android***")
    elif sys.platform == "ios":
        print("***No coverage report on iOS***")
    # Only print a coverage report if the test suite passed.
    elif app.returncode == 0:
        cov.stop()
        total = cov.report(
            precision=1,
            skip_covered=True,
            show_missing=True,
        )
        if total < 100.0:
            print("Test coverage is incomplete")
            # Uncomment the next line to enforce test coverage
            # TODO: app.returncode = 1

    app.add_background_task(lambda app, **kwargs: app.exit())


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

    # Start coverage tracking.
    # This needs to happen in the main thread, before the app has been created
    cov = coverage.Coverage(
        # Don't store any coverage data
        data_file=None,
        branch=True,
        source_pkgs=[toga_backend],
    )
    cov.start()

    # Create the test app, starting the test suite as a background task
    app = main()
    thread = Thread(target=partial(run_tests, app, cov))
    app.add_background_task(lambda app, *kwargs: thread.start())

    # Add an on_exit handler that will terminate the test suite.
    def exit_suite(app, **kwargs):
        print(f">>>>>>>>>> EXIT {app.returncode} <<<<<<<<<<")
        return True

    app.on_exit = exit_suite

    # Start the test app.
    app.main_loop()
