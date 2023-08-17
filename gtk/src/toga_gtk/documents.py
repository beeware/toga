class Document:  # pragma: no cover
    # GTK has 1-1 correspondence between document and app instances.
    SINGLE_DOCUMENT_APP = True

    def __init__(self, interface):
        self.interface = interface
        self.interface.read()
