import os
import subprocess
import sys
from pathlib import Path

import platformdirs
import pytest

import toga

USER_DIR_NAMES = ["desktop", "documents", "downloads", "pictures"]


def run_app(args, cwd, home):
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
            "TOGA_DUMMY_HOME": str(home),
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


def assert_paths(output, app_path, app_name, home):
    """Assert the paths for the standalone app are consistent."""
    results = output.splitlines()
    assert f"app.paths.app={app_path.resolve()}" in results
    full_name = f"org.testbed.{app_name}"
    assert f"app.paths.config={home / 'config' / full_name}" in results
    assert f"app.paths.data={home / 'user_data' / full_name}" in results
    assert f"app.paths.cache={home / 'cache' / full_name}" in results
    assert f"app.paths.logs={home / 'logs' / full_name}" in results
    assert f"app.paths.toga={Path(toga.__file__).parent.resolve()}" in results


def test_as_interactive(tmp_path):
    """At an interactive prompt, the app path is the current working directory."""
    # Spawn the interactive-mode mocking entry point
    cwd = Path(__file__).parent / "testbed"
    output = run_app(["interactive.py"], cwd=cwd, home=tmp_path)
    assert_paths(output, app_path=cwd, app_name="interactive-app", home=tmp_path)


def test_simple_as_file_in_module(tmp_path):
    """When a simple app is started as `python app.py` inside a runnable module, the app
    path is the folder holding app.py."""
    # Spawn the simple testbed app using `app.py`
    cwd = Path(__file__).parent / "testbed/simple"
    output = run_app(["app.py"], cwd=cwd, home=tmp_path)
    assert_paths(
        output,
        app_path=Path(toga.__file__).parent,
        app_name="simple-app",
        home=tmp_path,
    )


def test_simple_as_module(tmp_path):
    """When a simple apps is started as `python -m app` inside a runnable module, the
    app path is the folder holding app.py."""
    # Spawn the simple testbed app using `-m app`
    cwd = Path(__file__).parent / "testbed/simple"
    output = run_app(["-m", "app"], cwd=cwd, home=tmp_path)
    assert_paths(
        output,
        app_path=Path(toga.__file__).parent,
        app_name="simple-app",
        home=tmp_path,
    )


def test_simple_as_deep_file(tmp_path):
    """When a simple app is started as `python simple/app.py`, the app path is the
    folder holding app.py."""
    # Spawn the simple testbed app using `simple/app.py`
    cwd = Path(__file__).parent / "testbed"
    output = run_app(["simple/app.py"], cwd=cwd, home=tmp_path)
    assert_paths(
        output,
        app_path=Path(toga.__file__).parent,
        app_name="simple-app",
        home=tmp_path,
    )


def test_simple_as_deep_module(tmp_path):
    """When a simple app is started as `python -m simple`, the app path is the folder
    holding app.py."""
    # Spawn the simple testbed app using `-m simple`
    cwd = Path(__file__).parent / "testbed"
    output = run_app(["-m", "simple"], cwd=cwd, home=tmp_path)
    assert_paths(
        output,
        app_path=Path(toga.__file__).parent,
        app_name="simple-app",
        home=tmp_path,
    )


def test_subclassed_as_file_in_module(tmp_path):
    """When a subclassed app is started as `python app.py` inside a runnable module, the
    app path is the folder holding app.py."""
    # Spawn the simple testbed app using `app.py`
    cwd = Path(__file__).parent / "testbed/subclassed"
    output = run_app(["app.py"], cwd=cwd, home=tmp_path)
    assert_paths(output, app_path=cwd, app_name="subclassed-app", home=tmp_path)


def test_subclassed_as_module(tmp_path):
    """When a subclassed app is started as `python -m app` inside a runnable module, the
    app path is the folder holding app.py."""
    # Spawn the subclassed testbed app using `-m app`
    cwd = Path(__file__).parent / "testbed/subclassed"
    output = run_app(["-m", "app"], cwd=cwd, home=tmp_path)
    assert_paths(output, app_path=cwd, app_name="subclassed-app", home=tmp_path)


def test_subclassed_as_deep_file(tmp_path):
    """When a subclassed app is started as `python simple/app.py`, the app path is the
    folder holding app.py."""
    # Spawn the subclassed testbed app using `subclassed/app.py`
    cwd = Path(__file__).parent / "testbed"
    output = run_app(["subclassed/app.py"], cwd=cwd, home=tmp_path)
    assert_paths(
        output, app_path=cwd / "subclassed", app_name="subclassed-app", home=tmp_path
    )


def test_subclassed_as_deep_module(tmp_path):
    """When a subclassed app is started as `python -m simple`, the app path is the
    folder holding app.py."""
    # Spawn the subclassed testbed app using `-m subclassed`
    cwd = Path(__file__).parent / "testbed"
    output = run_app(["-m", "subclassed"], cwd=cwd, home=tmp_path)
    assert_paths(
        output, app_path=cwd / "subclassed", app_name="subclassed-app", home=tmp_path
    )


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


@pytest.mark.parametrize("name", USER_DIR_NAMES)
def test_user_dir(app, name, tmp_path):
    """User-space paths return the location provided by the backend."""
    (tmp_path / "toga-dummy" / name).mkdir(parents=True)

    assert getattr(app.paths, name) == tmp_path / "toga-dummy" / name


@pytest.mark.parametrize("name", USER_DIR_NAMES)
def test_user_dir_doesnt_exist(app, name, tmp_path):
    """If a user-space folder doesn't exist, accessing its path raises an error."""
    with pytest.raises(
        RuntimeError,
        match=rf"The {name.title()} folder .* does not exist on this device\.",
    ):
        getattr(app.paths, name)

    # The folder was not created by Toga.
    assert not (tmp_path / "toga-dummy" / name).exists()


@pytest.mark.parametrize("name", USER_DIR_NAMES)
def test_user_dir_default_location(app, name, monkeypatch):
    """Without the test override, the dummy backend puts paths in a dummy location."""
    monkeypatch.delenv("TOGA_DUMMY_HOME")

    impl_path = getattr(app.paths._impl, f"get_{name}_path")()
    assert impl_path == Path.home() / "toga-dummy" / name


class FakePlatformDirs:
    def __init__(self, root):
        self.user_config_path = root / "config"
        self.user_data_path = root / "data"
        self.user_cache_path = root / "cache"
        self.user_log_path = root / "logs"
        self.user_desktop_path = root / "desktop"
        self.user_documents_path = root / "documents"
        self.user_downloads_path = root / "downloads"
        self.user_pictures_path = root / "pictures"


def hide_backend_paths(monkeypatch):
    """Make the backend factory behave as if it has no Paths implementation."""
    factory = toga.platform.get_factory()
    # Ensure the entry points and the attribute cache are loaded.
    _ = factory.Paths
    monkeypatch.delattr(factory, "Paths")
    monkeypatch.delitem(factory._entrypoints, "Paths")


@pytest.fixture
async def platformdirs_app(monkeypatch, tmp_path):
    """An app using a backend that has no Paths implementation."""
    hide_backend_paths(monkeypatch)
    kwargs = {}

    def fake_platform_dirs(**kw):
        kwargs.update(kw)
        return FakePlatformDirs(tmp_path)

    monkeypatch.setattr(platformdirs, "PlatformDirs", fake_platform_dirs)
    app = toga.App(
        formal_name="Fallback App",
        app_id="org.testbed.fallback-app",
        author="Jane Developer",
    )
    return app, kwargs


@pytest.mark.parametrize("name", ["config", "data", "cache", "logs"])
def test_platformdirs_app_paths(platformdirs_app, name, tmp_path):
    """Without a backend paths module, app paths are provided by platformdirs."""
    app, kwargs = platformdirs_app

    path = getattr(app.paths, name)
    assert path == tmp_path / name
    # App-specific paths are created on first access.
    assert path.is_dir()
    # The platformdirs instance is configured for the app.
    assert kwargs == {"appname": "fallback-app", "appauthor": "Jane Developer"}


@pytest.mark.parametrize("name", USER_DIR_NAMES)
def test_platformdirs_user_dirs(platformdirs_app, name, tmp_path):
    """Without a backend paths module, user-space paths are provided by
    platformdirs."""
    app, _ = platformdirs_app
    (tmp_path / name).mkdir()

    assert getattr(app.paths, name) == tmp_path / name


async def test_platformdirs_no_author(monkeypatch, tmp_path):
    """If the app has no author, a placeholder author is used."""
    hide_backend_paths(monkeypatch)
    kwargs = {}

    def fake_platform_dirs(**kw):
        kwargs.update(kw)
        return FakePlatformDirs(tmp_path)

    monkeypatch.setattr(platformdirs, "PlatformDirs", fake_platform_dirs)
    app = toga.App(formal_name="Fallback App", app_id="org.testbed.fallback-app")

    assert app.paths.config == tmp_path / "config"
    assert kwargs["appauthor"] == "Unknown"
