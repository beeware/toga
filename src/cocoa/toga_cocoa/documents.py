from urllib.parse import quote

from rubicon.objc import objc_method

from toga_cocoa.libs import NSDocument, NSURL


class TogaDocument(NSDocument):
    @objc_method
    def autosavesInPlace(self) -> bool:
        return True

    @objc_method
    def readFromFileWrapper_ofType_error_(self, fileWrapper, typeName, outError) -> bool:
        self.interface.read()
        return True


class Document:
    def __init__(self, interface):
        self.native = TogaDocument.alloc()
        self.native.interface = interface
        self.native._impl = self

        self.native.initWithContentsOfURL(
            NSURL.URLWithString('file://{}'.format(quote(interface.filename))),
            ofType=interface.document_type,
            error=None
        )
