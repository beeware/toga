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

import testbed.app


def run_tests(app, cov, args, report_coverage, run_slow, running_in_ci):
    try:
        # Wait for the app's main window to be visible. Retrieving the actual
        # main window will raise an exception until the app is actually initialized.
        print("Waiting for app to be ready for testing... ", end="", flush=True)
        i = 0
        ready = False
        while i < 100 and not ready:
            try:
                main_window = app.main_window
                if main_window.visible:
                    ready = True
            except ValueError:
                pass

            time.sleep(0.05)
            i += 1

        if not ready:
            print("\nApp didn't display a main window.")
            app.returncode = 1
            return

        print("ready.")

        # Textual backend does not yet support testing.
        # However, this will verify a Textual app can at least start.
        if app.factory.__name__.startswith("toga_textual"):
            time.sleep(1)  # wait for the Textual app to start
            app.returncode = 0 if app._impl.native.is_running else 1
            return

        # Control the run speed of the test app.
        app.run_slow = run_slow

        project_path = Path(__file__).parent.parent
        os.chdir(project_path)

        os.environ["RUNNING_IN_CI"] = "true" if running_in_ci else ""

        app.returncode = pytest.main(
            [
                # Output formatting
                "-vv",
                "--no-header",
                "--tb=native",
                "--color=no",
                # Convert all warnings except for NotImplementedWarnings into errors
                "-Werror",
                "-Wignore::toga.NotImplementedWarning",
                # Run all async tests and fixtures using pytest-asyncio.
                "--asyncio-mode=auto",
                "--override-ini",
                "asyncio_default_fixture_loop_scope=session",
                # Override the cache directory to be somewhere known writable
                "--override-ini",
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
                    app.returncode = 1

    except BaseException:
        traceback.print_exc()
        app.returncode = 1
    finally:
        # Add a short pause to make sure any log tailing gets a chance to flush. Run a
        # couple of times to make sure any log streaming dropouts don't prevent
        # Briefcase from seeing the output.
        for i in range(0, 6):
            print(f">>>>>>>>>> EXIT {app.returncode} <<<<<<<<<<")
            time.sleep(0.5)
        app.loop.call_soon_threadsafe(app.exit)


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

    if "CI" in os.environ:
        data_file = (
            Path(os.environ["GITHUB_WORKSPACE"]) / "testbed" / "logs" / ".coverage"
        )
    else:
        data_file = None

    # Start coverage tracking.
    # This needs to happen in the main thread, before the app has been created
    cov = coverage.Coverage(
        data_file=data_file,
        branch=True,
        source_pkgs=[toga_backend],
    )
    cov.set_option("run:plugins", ["coverage_conditional_plugin"])
    cov.set_option(
        "coverage_conditional_plugin:rules",
        {
            "no-cover-if-linux-wayland": "os_environ.get('WAYLAND_DISPLAY', '') != ''",
            "no-cover-if-linux-x": (
                "os_environ.get('WAYLAND_DISPLAY', 'not-set') == 'not-set'"
            ),
        },
    )
    cov.start()

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

    # Use flag for running in CI since some tests will only succeed on the CI platform
    try:
        args.remove("--ci")
        running_in_ci = True
    except ValueError:
        running_in_ci = False

    # If there are no other specified arguments, default to running the whole suite,
    # and reporting coverage.
    if len(args) == 0:
        args = ["tests"]
        report_coverage = True

    # Create the test app, starting the test suite as a background task
    app = testbed.app.main()

    thread = Thread(
        target=partial(
            run_tests,
            app=app,
            cov=cov,
            args=args,
            run_slow=run_slow,
            report_coverage=report_coverage,
            running_in_ci=running_in_ci,
        )
    )

    # Queue a background task to run that will start the main thread. We do this,
    # instead of just starting the thread directly, so that we can make sure the App has
    # been fully initialized, and the event loop is running.
    app.loop.call_soon_threadsafe(thread.start)

    # Ensure Textual apps start in headless mode
    app._impl.headless = True

    # Start the test app
    app.main_loop()
