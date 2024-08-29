from pathlib import Path
from unittest.mock import Mock

import pytest

import toga
from toga.app import DocumentSet


class ExampleDocument(toga.Document):
    document_type = "Example Document"

    def create(self):
        self.main_document = Mock()

    def read(self):
        pass


@pytest.fixture
def document1(app):
    doc = ExampleDocument(app)
    doc._path = Path.cwd() / "somefile.txt"
    return doc


@pytest.fixture
def document2(app):
    return ExampleDocument(app)


def test_create(app):
    """An empty documentset can be created."""
    documentset = DocumentSet(app, [])

    assert len(documentset) == 0
    assert list(documentset) == []
    assert documentset.types == []


def test_create_with_types(app):
    """An documentset can be created with document types."""
    first_type = Mock(extensions=["first", "1st"])
    second_type = Mock(extensions=["second"])
    documentset = DocumentSet(app, [first_type, second_type])

    assert len(documentset) == 0
    assert list(documentset) == []
    assert documentset.types == [first_type, second_type]


def test_add_discard(app, document1, document2):
    """Documents can be added and removed to a documentset."""
    documentset = DocumentSet(app, [])

    # Add a document
    documentset._add(document2)
    assert len(documentset) == 1
    assert list(documentset) == [document2]

    # Add a second document; iteration order is creation order
    documentset._add(document1)
    assert len(documentset) == 2
    assert list(documentset) == [document2, document1]

    # Re-add a document that already exists
    with pytest.raises(ValueError, match=r"Document is already being managed."):
        documentset._add(document1)

    # Remove a document
    documentset._remove(document2)
    assert len(documentset) == 1
    assert list(documentset) == [document1]

    # Remove a document that isn't in the set
    with pytest.raises(ValueError, match=r"Document is not being managed."):
        documentset._remove(document2)


def test_retrieve(app, document1, document2):
    """Documents can be added and removed to a documentset."""
    documentset = DocumentSet(app, [])
    documentset._add(document2)
    documentset._add(document1)

    # Retrieve by index
    assert documentset[0] == document2
    assert documentset[1] == document1
    assert documentset[-2] == document2
    assert documentset[-1] == document1

    # Retrieve by path
    assert documentset[Path.cwd() / "somefile.txt"] == document1

    # Retrieve by string
    assert documentset[str(Path.cwd() / "somefile.txt")] == document1

    # Retrieve by non-absolute path
    assert documentset[Path("somefile.txt")] == document1

    # Retrieve by non-absolute path string
    assert documentset["somefile.txt"] == document1
