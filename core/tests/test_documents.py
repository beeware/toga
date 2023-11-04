from pathlib import Path

import pytest

import toga


class MyDoc(toga.Document):
    def __init__(self, path, app):
        super().__init__(path, "Dummy Document", app)
        pass

    def create(self):
        pass

    def read(self):
        pass


@pytest.mark.parametrize("path", ["/path/to/doc.mydoc", Path("/path/to/doc.mydoc")])
def test_create_document(app, path):
    doc = MyDoc(path, app)

    assert doc.path == Path(path)
    assert doc.app == app
    assert doc.document_type == "Dummy Document"


class MyDeprecatedDoc(toga.Document):
    def __init__(self, filename, app):
        super().__init__(
            path=filename,
            document_type="Deprecated Document",
            app=app,
        )

    def create(self):
        pass

    def read(self):
        pass


def test_deprecated_names(app):
    """Deprecated names still work."""
    doc = MyDeprecatedDoc("/path/to/doc.mydoc", app)

    with pytest.warns(
        DeprecationWarning,
        match=r"Document.filename has been renamed Document.path.",
    ):
        assert doc.filename == Path("/path/to/doc.mydoc")
