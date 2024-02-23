import os
from urllib.parse import quote

from toga_cocoa.libs import NSURL, NSDocument, objc_method, objc_property


class TogaDocument(NSDocument):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def autosavesInPlace(self) -> bool:
        return True

    @objc_method
    def readFromFileWrapper_ofType_error_(
        self, fileWrapper, typeName, outError
    ) -> bool:
        self.interface.read()
        return True


class Document:
    def __init__(self, interface):
        self.interface = interface
        self.native = TogaDocument.alloc()
        self.native.interface = interface
        self.native.impl = self

    def open(self):
        self.native.initWithContentsOfURL(
            NSURL.URLWithString(f"file://{quote(os.fsdecode(self.interface.path))}"),
            ofType=self.interface.document_type,
            error=None,
        )
