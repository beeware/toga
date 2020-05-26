
class Document:
    def __init__(self, filename, document_type, app=None):
        self.filename = filename
        self.document_type = document_type

        self._app = app

        # Create a platform specific implementation of the Document
        self._impl = app.factory.Document(interface=self)

    @property
    def app(self):
        return self._app

    def read(self):
        raise NotImplementedError('Document class must define read()')
