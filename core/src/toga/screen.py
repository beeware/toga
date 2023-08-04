class Screen:
    def __init__(self, _impl):
        self._impl = _impl

    @property
    def name(self):
        return self._impl.get_name()

    @property
    def origin(self):
        return self._impl.get_origin()
