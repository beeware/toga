import os
import subprocess
import sys
from pathlib import Path

import toga


def run_app(args, cwd):
    """Run a Toga app as a subprocess with coverage enabled and the Toga Dummy
    backend."""
    # We need to do a full copy of the environment, then add our extra bits;
    # if we don't the Windows interpreter won't inherit SYSTEMROOT
    env = os.environ.copy()
    env.update(
        {
            "COVERAGE_PROCESS_START": str(
                Path(__file__).parent.parent / "pyproject.toml"
            ),
            "PYTHONPATH": str(Path(__file__).parent / "testbed/customize"),
            "TOGA_BACKEND": "toga_dummy",
        }
    )
    output = subprocess.check_output(
        [sys.executable] + args,
        cwd=cwd,
        env=env,
        text=True,
    )
    # When called as a subprocess, coverage drops its coverage report in CWD.
    # Move it to the project root for combination with the main test report.
    for file in cwd.glob(".coverage*"):
        os.rename(file, Path(__file__).parent.parent / file.name)
    return output


def assert_paths(output, app_path, app_name):
    """Assert the paths for the standalone app are consistent."""
    results = output.splitlines()
    assert f"app.paths.app={app_path.resolve()}" in results
    assert (
        f"app.paths.config={(Path.home() / 'config' / f'org.testbed.{app_name}').resolve()}"
        in results
    )
    assert (
        f"app.paths.data={(Path.home() / 'user_data' / f'org.testbed.{app_name}').resolve()}"
        in results
    )
    assert (
        f"app.paths.cache={(Path.home() / 'cache' / f'org.testbed.{app_name}').resolve()}"
        in results
    )
    assert (
        f"app.paths.logs={(Path.home() / 'logs' / f'org.testbed.{app_name}').resolve()}"
        in results
    )
    assert f"app.paths.toga={Path(toga.__file__).parent.resolve()}" in results


def test_as_interactive():
    """At an interactive prompt, the app path is the current working directory."""
    # Spawn the interactive-mode mocking entry point
    cwd = Path(__file__).parent / "testbed"
    output = run_app(["interactive.py"], cwd=cwd)
    assert_paths(output, app_path=cwd, app_name="interactive-app")


def test_simple_as_file_in_module():
    """When a simple app is started as `python app.py` inside a runnable module, the app
    path is the folder holding app.py."""
    # Spawn the simple testbed app using `app.py`
    cwd = Path(__file__).parent / "testbed/simple"
    output = run_app(["app.py"], cwd=cwd)
    assert_paths(output, app_path=Path(toga.__file__).parent, app_name="simple-app")


def test_simple_as_module():
    """When a simple apps is started as `python -m app` inside a runnable module, the
    app path is the folder holding app.py."""
    # Spawn the simple testbed app using `-m app`
    cwd = Path(__file__).parent / "testbed/simple"
    output = run_app(["-m", "app"], cwd=cwd)
    assert_paths(output, app_path=Path(toga.__file__).parent, app_name="simple-app")


def test_simple_as_deep_file():
    """When a simple app is started as `python simple/app.py`, the app path is the
    folder holding app.py."""
    # Spawn the simple testbed app using `simple/app.py`
    cwd = Path(__file__).parent / "testbed"
    output = run_app(["simple/app.py"], cwd=cwd)
    assert_paths(output, app_path=Path(toga.__file__).parent, app_name="simple-app")


def test_simple_as_deep_module():
    """When a simple app is started as `python -m simple`, the app path is the folder
    holding app.py."""
    # Spawn the simple testbed app using `-m simple`
    cwd = Path(__file__).parent / "testbed"
    output = run_app(["-m", "simple"], cwd=cwd)
    assert_paths(output, app_path=Path(toga.__file__).parent, app_name="simple-app")


def test_subclassed_as_file_in_module():
    """When a subclassed app is started as `python app.py` inside a runnable module, the
    app path is the folder holding app.py."""
    # Spawn the simple testbed app using `app.py`
    cwd = Path(__file__).parent / "testbed/subclassed"
    output = run_app(["app.py"], cwd=cwd)
    assert_paths(output, app_path=cwd, app_name="subclassed-app")


def test_subclassed_as_module():
    """When a subclassed app is started as `python -m app` inside a runnable module, the
    app path is the folder holding app.py."""
    # Spawn the subclassed testbed app using `-m app`
    cwd = Path(__file__).parent / "testbed/subclassed"
    output = run_app(["-m", "app"], cwd=cwd)
    assert_paths(output, app_path=cwd, app_name="subclassed-app")


def test_subclassed_as_deep_file():
    """When a subclassed app is started as `python simple/app.py`, the app path is the
    folder holding app.py."""
    # Spawn the subclassed testbed app using `subclassed/app.py`
    cwd = Path(__file__).parent / "testbed"
    output = run_app(["subclassed/app.py"], cwd=cwd)
    assert_paths(output, app_path=cwd / "subclassed", app_name="subclassed-app")


def test_subclassed_as_deep_module():
    """When a subclassed app is started as `python -m simple`, the app path is the
    folder holding app.py."""
    # Spawn the subclassed testbed app using `-m subclassed`
    cwd = Path(__file__).parent / "testbed"
    output = run_app(["-m", "subclassed"], cwd=cwd)
    assert_paths(output, app_path=cwd / "subclassed", app_name="subclassed-app")
