import unittest
import subprocess
import sys
from pathlib import Path

import toga
import toga_dummy


class TestPaths(unittest.TestCase):
    def setUp(self):
        # We use the existence of a __main__ module as a proxy for being in test
        # conditions. This isn't *great*, but the __main__ module isn't meaningful
        # during tests, and removing it allows us to avoid having explicit "if
        # under test conditions" checks in paths.py.
        if '__main__' in sys.modules:
            del sys.modules['__main__']

    def assert_paths(self, output, app_path, app_name):
        "Assert the paths for the standalone app are consistent"
        results = output.splitlines()
        self.assertIn(
            f"app.paths.app={app_path.resolve()}",
            results,
        )
        self.assertIn(
            f"app.paths.data={(Path.home() / 'user_data' / f'org.testbed.{app_name}').resolve()}",
            results,
        )
        self.assertIn(
            f"app.paths.cache={(Path.home() / 'cache' / f'org.testbed.{app_name}').resolve()}",
            results,
        )
        self.assertIn(
            f"app.paths.logs={(Path.home() / 'logs' / f'org.testbed.{app_name}').resolve()}",
            results,
        )
        self.assertIn(
            f"app.paths.toga={Path(toga.__file__).parent.resolve()}",
            results,
        )

    def test_as_test(self):
        "During test conditions, the app path is the current working directory"
        app = toga.App(
            formal_name="Test App",
            app_id="org.beeware.test-app",
            factory=toga_dummy.factory,
        )

        self.assertEqual(
            app.paths.app,
            Path.cwd(),
        )
        self.assertEqual(
            app.paths.data,
            Path.home() / "user_data" / "org.beeware.test-app",
        )
        self.assertEqual(
            app.paths.cache,
            Path.home() / "cache" / "org.beeware.test-app",
        )
        self.assertEqual(
            app.paths.logs,
            Path.home() / "logs" / "org.beeware.test-app",
        )
        self.assertEqual(
            app.paths.toga,
            Path(toga.__file__).parent,
        )

    def test_as_interactive(self):
        "At an interactive prompt, the app path is the current working directory"
        # Spawn the standalone app using the interactive-mode mocking entry point
        cwd = Path(__file__).parent / "testbed"
        output = subprocess.check_output(
            [sys.executable, "standalone.py", "--backend:dummy", "--interactive"],
            cwd=cwd,
            text=True,
        )
        self.assert_paths(output, app_path=cwd, app_name="standalone-app")

    def test_as_file(self):
        "When started as `python app.py`, the app path is the folder holding app.py"
        # Spawn the standalone app using `standalone.py`
        cwd = Path(__file__).parent / "testbed"
        output = subprocess.check_output(
            [sys.executable, "standalone.py", "--backend:dummy"],
            cwd=cwd,
            text=True,
        )
        self.assert_paths(output, app_path=cwd, app_name="standalone-app")

    def test_as_module(self):
        "When started as `python -m app`, the app path is the folder holding app.py"
        # Spawn the standalone app app using `-m standalone`
        cwd = Path(__file__).parent / "testbed"
        output = subprocess.check_output(
            [sys.executable, "-m", "standalone", "--backend:dummy"],
            cwd=cwd,
            text=True,
        )
        self.assert_paths(output, app_path=cwd, app_name="standalone-app")

    def test_simple_as_file_in_module(self):
        """When a simple app is started as `python app.py` inside a runnable module,
        the app path is the folder holding app.py"""
        # Spawn the simple testbed app using `app.py`
        cwd = Path(__file__).parent / "testbed" / "simple"
        output = subprocess.check_output(
            [sys.executable, "app.py", "--backend:dummy"],
            cwd=cwd,
            text=True,
        )
        self.assert_paths(output, app_path=cwd, app_name="simple-app")

    def test_simple_as_module(self):
        """When a simple apps is started as `python -m app` inside a runnable module,
        the app path is the folder holding app.py"""
        # Spawn the simple testbed app using `-m app`
        cwd = Path(__file__).parent / "testbed" / "simple"
        output = subprocess.check_output(
            [sys.executable, "-m", "app", "--backend:dummy"],
            cwd=cwd,
            text=True,
        )
        self.assert_paths(output, app_path=cwd, app_name="simple-app")

    def test_simple_as_deep_file(self):
        "When a simple app is started as `python simple/app.py`, the app path is the folder holding app.py"
        # Spawn the simple testbed app using `-m simple`
        cwd = Path(__file__).parent / "testbed"
        output = subprocess.check_output(
            [sys.executable, "simple/app.py", "--backend:dummy"],
            cwd=cwd,
            text=True,
        )
        self.assert_paths(output, app_path=cwd / "simple", app_name="simple-app")

    def test_simple_as_deep_module(self):
        "When a simple app is started as `python -m simple`, the app path is the folder holding app.py"
        # Spawn the simple testbed app using `-m simple`
        cwd = Path(__file__).parent / "testbed"
        output = subprocess.check_output(
            [sys.executable, "-m", "simple", "--backend:dummy"],
            cwd=cwd,
            text=True,
        )
        self.assert_paths(output, app_path=cwd / "simple", app_name="simple-app")

    def test_installed_as_module(self):
        "When the installed app is started, the app path is the folder holding app.py"
        # Spawn the installed testbed app using `-m app`
        cwd = Path(__file__).parent / "testbed"
        output = subprocess.check_output(
            [sys.executable, "-m", "installed", "--backend:dummy"],
            cwd=cwd,
            text=True,
        )

        self.assert_paths(output, app_path=cwd / "installed", app_name="installed")
