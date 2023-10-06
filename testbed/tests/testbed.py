import errno
import os
import sys
import tempfile
import time
import traceback
from functools import partial
from pathlib import Path
from threading import Thread

import coverage
import pytest

from testbed.app import main


def run_tests(app, cov, args, report_coverage, run_slow):
    try:
        # Wait for the app's main window to be visible.
        print("Waiting for app to be ready for testing... ", end="", flush=True)
        while app.main_window is None or not app.main_window.visible:
            time.sleep(0.05)
        print("ready.")
        # Control the run speed of the test app.
        app.run_slow = run_slow

        project_path = Path(__file__).parent.parent
        os.chdir(project_path)

        app.returncode = pytest.main(
            [
                # Output formatting
                "-vv",
                "--no-header",
                "--tb=native",
                "--color=no",
                # Run all async tests and fixtures using pytest-asyncio.
                "--asyncio-mode=auto",
                # Override the cache directory to be somewhere known writable
                "-o",
                f"cache_dir={tempfile.gettempdir()}/.pytest_cache",
            ]
            + args
        )

        # WORKAROUND: On Android, the main thread where coverage has been started
        # dies before this thread; as a result, the garbage collection on the tracer
        # function raises an IndexError because the data stack is empty for that
        # thread. This has been reported as
        # https://github.com/nedbat/coveragepy/issues/1542 and a PR submitted; This
        # workaround can be removed once that PR is available in a production
        # version of coverage.
        #
        # Desktop platforms use CTracer, which doesn't have a data_stack attribute, but
        # that's OK because desktop platforms don't have this threading issue anyway.
        for tracer in cov._collector.tracers:
            if hasattr(tracer, "data_stack") and len(tracer.data_stack) == 0:
                print("Backfilling empty coverage stack...")
                tracer.data_stack.append((None, None, None, None))

        # Only print a coverage report if the test suite passed.
        if app.returncode == 0:
            cov.stop()
            if report_coverage:
                # Exclude some patterns of lines that can't have coverage
                cov.exclude("pragma: no cover")
                cov.exclude("@(abc\\.)?abstractmethod")
                cov.exclude("NotImplementedError")
                cov.exclude("\\.not_implemented\\(")

                total = cov.report(
                    precision=1,
                    skip_covered=True,
                    show_missing=True,
                )
                if total < 100.0:
                    print("Test coverage is incomplete")
                    # Uncomment the next line to enforce test coverage
                    # TODO: app.returncode = 1
    except BaseException:
        traceback.print_exc()
        app.returncode = 1
    finally:
        print(f">>>>>>>>>> EXIT {app.returncode} <<<<<<<<<<")
        # Add a short pause to make sure any log tailing gets a chance to flush
        time.sleep(0.5)
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

    if toga_backend == "toga_android":
        # Prevent the log being cluttered with "avc: denied" messages
        # (https://github.com/beeware/toga/issues/1962).
        def get_terminal_size(*args, **kwargs):
            error = errno.ENOTTY
            raise OSError(error, os.strerror(error))

        os.get_terminal_size = get_terminal_size

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

    # Determine pytest arguments
    args = sys.argv[1:]

    # If `--slow` is in the arguments, run the test suite in slow mode
    try:
        args.remove("--slow")
        args.append("-s")
        run_slow = True
    except ValueError:
        run_slow = False

    # If `--coverage` is in the arguments, display a coverage report
    try:
        args.remove("--coverage")
        report_coverage = True
    except ValueError:
        report_coverage = False

    # If there are no other specified arguments, default to running the whole suite,
    # and reporting coverage.
    if len(args) == 0:
        args = ["tests"]
        report_coverage = True

    thread = Thread(
        target=partial(
            run_tests,
            app=app,
            cov=cov,
            args=args,
            run_slow=run_slow,
            report_coverage=report_coverage,
        )
    )
    thread.start()

    # Start the test app.
    app.main_loop()
