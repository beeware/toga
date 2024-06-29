from pathlib import Path

import pytest

import toga

####################################################################################
# Document API tests
####################################################################################
if toga.platform.current_platform not in {"macOS", "windows", "linux"}:
    pytest.skip(
        "Document API is specific to desktop platforms", allow_module_level=True
    )


async def test_open_document(app, app_probe):
    """A document can be opened."""
    try:
        # A document can be opened
        document_path = Path(__file__).parent / "docs/example.testbed"
        app.open(document_path)

        await app_probe.redraw("Document has been opened")

        assert len(app.documents) == 1
        assert len(app.windows) == 2

        # Document has been read.
        app.documents[0]._content.read.assert_called_with(document_path)
    finally:
        for document in app.documents:
            document.main_window.close()
        await app_probe.redraw("Document windows have been closed")


async def test_open_missing_document(app, app_probe):
    """If an attempt is made to open a missing file, an error is raised."""
    try:
        # If the file doesn't exist, an exception is raised
        with pytest.raises(FileNotFoundError):
            app.open(Path(__file__).parent / "docs/does_not_exist.testbed")

        await app_probe.redraw("Attempt to open a missing document has been made")

        # No document or document window has been opened
        assert len(app.documents) == 0
        assert len(app.windows) == 1
    finally:
        for document in app.documents:
            document.main_window.close()
        await app_probe.redraw("Document windows have been closed")


async def test_open_bad_document(app, app_probe, capsys):
    """If an error is raised reading a file, an error is raised."""
    try:
        # A document can be opened
        document_path = Path(__file__).parent / "docs/broken.testbed"
        with pytest.raises(
            RuntimeError,
            match=r"Unable to load broken document",
        ):
            app.open(document_path)

        await app_probe.redraw("Attempt to open a bad document has been made")

        # No document or document window has been opened
        assert len(app.documents) == 0
        assert len(app.windows) == 1
    finally:
        for document in app.documents:
            document.main_window.close()
        await app_probe.redraw("Document windows have been closed")


async def test_open_initial_document(monkeypatch, app, app_probe):
    """An initial document can be opened."""
    try:
        # Trigger the opening of the initial document
        assert await app_probe.assert_open_initial_document(monkeypatch)

    finally:
        for document in app.documents:
            document.main_window.close()
        await app_probe.redraw("Document windows have been closed")


async def test_open_document_by_drag(app, app_probe):
    """A file can be If an attempt is made to open a file by dragging, an error is raised."""
    try:
        document_path = Path(__file__).parent / "docs/example.testbed"
        app_probe.open_document_by_drag(document_path)

        await app_probe.redraw("Document has been opened by drag", delay=1)

        assert len(app.documents) == 1
        assert len(app.windows) == 2

        # Document has been read.
        app.documents[0]._content.read.assert_called_with(document_path)

    finally:
        for document in app.documents:
            document.main_window.close()
        await app_probe.redraw("Document windows have been closed")
