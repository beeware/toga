import sys
import tempfile
import threading
from functools import partial

import pytest

import tests
import toga


class TogaTest(toga.App):
    def startup(self):
        # For the "app" fixture.
        global app
        app = self

        self.main_box = toga.Box()

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = self.main_box
        self.main_window.show()

        threading.Thread(target=partial(test, self)).start()


def test(app):
    if hasattr(sys, "getandroidapilevel"):
        chaquopy_extract_package(tests)

    pytest.main(
        [
            # Output formatting
            "-vv",
            "--no-header",
            "--tb=native",
            "-rP",
            "--color=no",  # Color codes mess up the output on MSYS2, even with `winpty`.
            # Run all async tests and fixtures using pytest-asyncio.
            "--asyncio-mode=auto",
            # Override the cache directory to be somewhere known writable
            "-o",
            f"cache_dir={tempfile.gettempdir()}/.pytest_cache",
        ]
        + tests.__path__
    )
    app.add_background_task(lambda app: app.exit())


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


def main():
    return TogaTest()
