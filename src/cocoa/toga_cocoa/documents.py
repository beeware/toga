from rubicon.objc import objc_method

from toga_cocoa.libs import NSDocument, NSURL


class TogaDocument(NSDocument):
    @objc_method
    def autosavesInPlace(self) -> bool:
        return True

    @objc_method
    def readFromFileWrapper_ofType_error_(self, fileWrapper, typeName, outError) -> bool:
        print("Read from File Wrapper: %s" % fileWrapper.filename)
        print("   type: %s" % typeName)

        try:
            self.interface.read(fileWrapper.filename)
            return True
        except:
            return False
        # if fileWrapper.isDirectory:
        #     # Multi-file .podium files must contain slides.md; may contain theme.css
        #     themeFile = fileWrapper.fileWrappers.valueForKey("theme.css")
        #     contentFile = fileWrapper.fileWrappers.valueForKey("slides.md")
        #     if contentFile is None:
        #         return False

        #     self.content = cast(contentFile.regularFileContents.bytes, c_char_p).value.decode('utf-8')
        #     if themeFile is None:
        #         self.theme = None
        #     else:
        #         self.theme = cast(themeFile.regularFileContents.bytes, c_char_p).value.decode('utf-8')

        #     return True

        return False


class Document:
    def __init__(self, interface):
        self.native = TogaDocument.alloc()
        self.native.interface = interface
        self.native._impl = self

        self.native.initWithContentsOfURL(
            NSURL.URLWithString(interface.url),
            ofType=interface.document_type,
            error=None
        )
