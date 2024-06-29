import os
from urllib.parse import quote

from toga_cocoa.libs import NSURL, NSDocument, objc_method, objc_property


class TogaDocument(NSDocument):
    interface = objc_property(object, weak=True)
    impl = objc_property(object, weak=True)

    @objc_method
    def readFromFileWrapper_ofType_error_(
        self, fileWrapper, typeName, outError
    ) -> bool:
        try:
            self.interface.read()
            return True
        except Exception as e:
            self.impl.error = e
            return False


class Document:
    def __init__(self, interface):
        self.interface = interface
        self.native = None
        self.error = None

    def open(self):
        if self.interface.path.exists():
            # This is a little odd; we need to alloc the object, then set interface/impl
            # attributes so that the init call can use those attributes. We need an
            # additional retain because of reference cycles inside Cocoa's document
            # handling; we need to make sure Toga's reference is the last deletion.
            self.native = TogaDocument.alloc().retain()
            self.native.interface = self.interface
            self.native.impl = self

            self.native.initWithContentsOfURL(
                NSURL.URLWithString(
                    f"file://{quote(os.fsdecode(self.interface.path))}"
                ),
                ofType=self.interface.document_type,
                error=None,
            )
            if self.error:
                raise self.error
        else:
            raise FileNotFoundError()

    def __del__(self):
        if self.native:
            self.native.release()
