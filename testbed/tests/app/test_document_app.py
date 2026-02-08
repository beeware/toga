from pathlib import Path

import pytest

import toga
from testbed.app import ExampleDoc

####################################################################################
# Document API tests
####################################################################################
if toga.platform.current_platform not in {"macOS", "windows", "linux"}:
    pytest.skip(
        "Document API is specific to desktop platforms", allow_module_level=True
    )


async def test_new_document(app, app_probe):
    """A new document can be created."""
    # Create a new document
    app.documents.new(ExampleDoc)

    await app_probe.redraw("New document has been created")

    assert len(app.documents) == 1
    assert len(app.windows) == 2

    # Document has not been read
    app.documents[0]._content.read.assert_not_called()
    assert app.documents[0].title == "Example Document: Untitled"


async def test_open_document(app, app_probe):
    """A document can be opened."""
    # A document can be opened
    document_path = Path(__file__).parent / "docs/example.testbed"
    app.documents.open(document_path)

    await app_probe.redraw("Document has been opened", delay=0.2)

    assert len(app.documents) == 1
    assert len(app.windows) == 2

    # Document has been read.
    app.documents[0]._content.read.assert_called_with(document_path)


async def test_open_missing_document(app, app_probe):
    """If an attempt is made to open a missing file, an error is raised."""
    # If the file doesn't exist, an exception is raised
    with pytest.raises(FileNotFoundError):
        app.documents.open(Path(__file__).parent / "docs/does_not_exist.testbed")

    await app_probe.redraw("Attempt to open a missing document has been made")

    # No document or document window has been opened
    assert len(app.documents) == 0
    assert len(app.windows) == 1


async def test_open_bad_document(app, app_probe, capsys):
    """If an error is raised reading a file, an error is raised."""
    # A document can be opened
    document_path = Path(__file__).parent / "docs/broken.testbed"
    with pytest.raises(
        RuntimeError,
        match=r"Unable to load broken document",
    ):
        app.documents.open(document_path)

    await app_probe.redraw("Attempt to open a bad document has been made")

    # No document or document window has been opened
    assert len(app.documents) == 0
    assert len(app.windows) == 1


async def test_open_initial_document(monkeypatch, app, app_probe):
    """An initial document can be opened."""
    document_path = Path(__file__).parent / "docs/example.testbed"

    # Trigger the opening of the initial document. What this means is platform
    # dependent, so trust the probe to validate what this means
    await app_probe.open_initial_document(monkeypatch, document_path)

    assert len(app.documents) == 1
    assert len(app.windows) == 2

    # Document has been read.
    app.documents[0]._content.read.assert_called_with(document_path)


async def test_open_document_by_drag(app, app_probe):
    """A file can be opened by dragging."""
    document_path = Path(__file__).parent / "docs/example.testbed"
    app_probe.open_document_by_drag(document_path)

    await app_probe.redraw("Document has been opened by drag", delay=1)

    assert len(app.documents) == 1
    assert len(app.windows) == 2

    # Document has been read.
    app.documents[0]._content.read.assert_called_with(document_path)


async def test_save_document(app, app_probe):
    """A document can be saved."""
    # A document can be opened
    document_path = Path(__file__).parent / "docs/example.testbed"
    app.documents.open(document_path)

    await app_probe.redraw("Document has been opened", delay=0.2)

    assert len(app.documents) == 1
    assert len(app.windows) == 2

    # Document has been read.
    app.documents[0]._content.read.assert_called_with(document_path)

    # Save the document
    await app.documents.save()
    await app_probe.redraw("Document has been saved")

    # Document has been saved.
    app.documents[0]._content.write.assert_called_with(document_path)


async def test_save_as_document(monkeypatch, app, app_probe, tmp_path):
    """A document can be saved under a new filename."""

    # A document can be opened
    document_path = Path(__file__).parent / "docs/example.testbed"
    document = app.documents.open(document_path)

    # Monkeypatch the save_as dialog handling so that a dialog isn't activated.
    async def mock_save_as_dialog(dialog):
        return tmp_path / "new_filename.testbed"

    monkeypatch.setattr(document.main_window, "dialog", mock_save_as_dialog)

    await app_probe.redraw("Document has been opened", delay=0.2)

    assert len(app.documents) == 1
    assert len(app.windows) == 2

    # Document has been read.
    app.documents[0]._content.read.assert_called_with(document_path)

    # Save the document in a new location
    await app.documents.save_as()
    await app_probe.redraw("Document has been saved with a new filename")

    # Document has been saved in a new location
    app.documents[0]._content.write.assert_called_with(
        tmp_path / "new_filename.testbed"
    )


async def test_save_all_documents(app, app_probe):
    """All documents can be saved."""
    # A document can be opened
    document_path = Path(__file__).parent / "docs/example.testbed"
    app.documents.open(document_path)

    await app_probe.redraw("Document has been opened", delay=0.2)

    assert len(app.documents) == 1
    assert len(app.windows) == 2

    # Document has been read.
    app.documents[0]._content.read.assert_called_with(document_path)

    # Save all windows in the app
    await app.documents.save_all()
    await app_probe.redraw("Save All has been invoked")

    # Document has been saved.
    app.documents[0]._content.write.assert_called_with(document_path)
