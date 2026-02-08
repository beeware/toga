from unittest.mock import Mock

import pytest

import toga


@pytest.fixture
def mock_app_exit(monkeypatch, app):
    # We can't actually exit during a test, so monkeypatch the exit call.
    app_exit = Mock()
    monkeypatch.setattr(toga.App, "exit", app_exit)
    return app_exit


@pytest.fixture
def mock_main_window_close(monkeypatch, main_window):
    # We need to prevent the main window from *actually* closing, so monkeypatch the
    # method that implements the actual close.

    window_close = Mock()

    monkeypatch.setattr(main_window, "_close", window_close)

    return window_close
