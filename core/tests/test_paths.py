import os
import subprocess
import sys
from pathlib import Path

import pytest

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
        encoding="utf-8",
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
    home = Path.home()
    full_name = f"org.testbed.{app_name}"
    assert f"app.paths.config={home / 'config' / full_name}" in results
    assert f"app.paths.data={home / 'user_data' / full_name}" in results
    assert f"app.paths.cache={home / 'cache' / full_name}" in results
    assert f"app.paths.logs={home / 'logs' / full_name}" in results
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


@pytest.mark.parametrize(
    "path_name",
    [
        "toga",
        "app",
        "config",
        "data",
        "cache",
        "logs",
        "desktop",
        "documents",
        "downloads",
        "pictures",
    ],
)
def test_cant_reassign(app, path_name):
    """App path attributes are read-only."""
    # Theoretically, this could leak out of this test... but only if it fails!
    with pytest.raises(AttributeError):
        setattr(app.paths, path_name, "")


@pytest.mark.parametrize("name", ["desktop", "documents", "downloads", "pictures"])
def test_user_dir(app, name, tmp_path, monkeypatch):
    """User-space paths return the location provided by the backend."""
    monkeypatch.setenv("TOGA_DUMMY_USER_DIRS", str(tmp_path))
    (tmp_path / name).mkdir()

    assert getattr(app.paths, name) == tmp_path / name


@pytest.mark.parametrize("name", ["desktop", "documents", "downloads", "pictures"])
def test_user_dir_doesnt_exist(app, name, tmp_path, monkeypatch):
    """If a user-space folder doesn't exist, accessing its path raises an error."""
    monkeypatch.setenv("TOGA_DUMMY_USER_DIRS", str(tmp_path))

    # The folder is *not* created by Toga.
    with pytest.raises(
        RuntimeError,
        match=rf"The {name.title()} folder .* does not exist on this device\.",
    ):
        getattr(app.paths, name)
    assert not (tmp_path / name).exists()


@pytest.mark.parametrize("name", ["desktop", "documents", "downloads", "pictures"])
def test_user_dir_default_location(app, name, monkeypatch):
    """Without the test override, the dummy backend puts user-space folders in a
    clearly dummy location."""
    monkeypatch.delenv("TOGA_DUMMY_USER_DIRS", raising=False)

    impl_path = getattr(app.paths._impl, f"get_{name}_path")()
    assert impl_path == Path.home() / "toga-dummy" / name
