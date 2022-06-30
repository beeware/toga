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

    def assert_standalone_paths(self, output):
        "Assert the paths for the standalone app are consistent"
        results = output.splitlines()
        self.assertIn(
            f"app.paths.app={Path.cwd() / 'tests' / 'testbed'}",
            results,
        )
        self.assertIn(
            f"app.paths.data={Path.home() / 'user_data' / 'org.testbed.standalone-app'}",
            results,
        )
        self.assertIn(
            f"app.paths.cache={Path.home() / 'cache' / 'org.testbed.standalone-app'}",
            results,
        )
        self.assertIn(
            f"app.paths.logs={Path.home() / 'logs' / 'org.testbed.standalone-app'}",
            results,
        )
        self.assertIn(
            f"app.paths.toga={Path(toga.__file__).parent}",
            results,
        )

    def test_as_interactive(self):
        "At an interactive prompt, the app path is the current working directory"
        # Spawn the standalone app using the interactive-mode mocking entry point
        output = subprocess.check_output(
            [sys.executable, "standalone.py", "--backend:dummy", "--interactive"],
            cwd=Path(__file__).parent / "testbed",
            text=True,
        )
        self.assert_standalone_paths(output)

    def test_as_file(self):
        "When started as `python app.py`, the app path is the folder holding app.py"
        # Spawn the standalone app using `standalone.py`
        output = subprocess.check_output(
            [sys.executable, "standalone.py", "--backend:dummy"],
            cwd=Path(__file__).parent / "testbed",
            text=True,
        )
        self.assert_standalone_paths(output)

    def test_as_module(self):
        "When started as `python -m app`, the app path is the folder holding app.py"
        # Spawn the standalone app app using `-m standalone`
        output = subprocess.check_output(
            [sys.executable, "-m", "standalone", "--backend:dummy"],
            cwd=Path(__file__).parent / "testbed",
            text=True,
        )
        self.assert_standalone_paths(output)

    def assert_simple_paths(self, output):
        "Assert the paths for the simple app are consistent"
        results = output.splitlines()
        self.assertIn(
            f"app.paths.app={Path.cwd() / 'tests' / 'testbed' / 'simple'}",
            results,
        )
        self.assertIn(
            f"app.paths.data={Path.home() / 'user_data' / 'org.testbed.simple-app'}",
            results,
        )
        self.assertIn(
            f"app.paths.cache={Path.home() / 'cache' / 'org.testbed.simple-app'}",
            results,
        )
        self.assertIn(
            f"app.paths.logs={Path.home() / 'logs' / 'org.testbed.simple-app'}", results
        )
        self.assertIn(
            f"app.paths.toga={Path(toga.__file__).parent}",
            results,
        )

    def test_simple_as_file_in_module(self):
        """When a simple app is started as `python app.py` inside a runnable module,
        the app path is the folder holding app.py"""
        # Spawn the simple testbed app using `app.py`
        output = subprocess.check_output(
            [sys.executable, "app.py", "--backend:dummy"],
            cwd=Path(__file__).parent / "testbed" / "simple",
            text=True,
        )
        self.assert_simple_paths(output)

    def test_simple_as_module(self):
        """When a simple apps is started as `python -m app` inside a runnable module,
        the app path is the folder holding app.py"""
        # Spawn the simple testbed app using `-m app`
        output = subprocess.check_output(
            [sys.executable, "-m", "app", "--backend:dummy"],
            cwd=Path(__file__).parent / "testbed" / "simple",
            text=True,
        )
        self.assert_simple_paths(output)

    def test_simple_as_deep_file(self):
        "When a simple app is started as `python simple/app.py`, the app path is the folder holding app.py"
        # Spawn the simple testbed app using `-m simple`
        output = subprocess.check_output(
            [sys.executable, "simple/app.py", "--backend:dummy"],
            cwd=Path(__file__).parent / "testbed",
            text=True,
        )
        self.assert_simple_paths(output)

    def test_simple_as_deep_module(self):
        "When a simple app is started as `python -m simple`, the app path is the folder holding app.py"
        # Spawn the simple testbed app using `-m simple`
        output = subprocess.check_output(
            [sys.executable, "-m", "simple", "--backend:dummy"],
            cwd=Path(__file__).parent / "testbed",
            text=True,
        )
        self.assert_simple_paths(output)

    def test_installed_as_module(self):
        "When the installed app is started, the app path is the folder holding app.py"
        # Spawn the installed testbed app using `-m app`
        output = subprocess.check_output(
            [sys.executable, "-m", "installed", "--backend:dummy"],
            cwd=Path(__file__).parent / "testbed",
            text=True,
        )

        results = output.splitlines()
        self.assertIn(
            f"app.paths.app={Path.cwd() / 'tests' / 'testbed' / 'installed'}",
            results,
        )
        self.assertIn(
            f"app.paths.data={Path.home() / 'user_data' / 'org.testbed.installed'}",
            results,
        )
        self.assertIn(
            f"app.paths.cache={Path.home() / 'cache' / 'org.testbed.installed'}",
            results,
        )
        self.assertIn(
            f"app.paths.logs={Path.home() / 'logs' / 'org.testbed.installed'}",
            results,
        )
        self.assertIn(f"app.paths.toga={Path(toga.__file__).parent}", results)
