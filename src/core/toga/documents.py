

class Document:
    def __init__(self, url, document_type, factory=None):
        self.factory = factory
        self.url = url
        self.document_type = document_type

        self._app = None

        # Create a platform specific implementation of the Document
        self._impl = self.factory.Document(interface=self)

    @property
    def app(self):
        return self._app

    @app.setter
    def app(self, app):
        if self._app:
            raise Exception("Document is already associated with an App")

        self._app = app
        self.set_app(app)

    def _set_app(self, app):
        pass

    def read(self, filename):
        raise NotImplementedError('Document class must define read()')
