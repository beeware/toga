from .base_proxy import BaseProxy


class AppProxy(BaseProxy):
    def __init__(self):
        super().__init__("self")
