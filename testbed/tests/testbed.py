import os
import tempfile
from functools import partial
from pathlib import Path
from threading import Thread

import pytest

from testbed.app import main


def run_tests(app):
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
    app.add_background_task(lambda app, **kwargs: app.exit())


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
