import os


class Singtools(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(cls, *args, **kwargs)
        return cls._instance


class ManagerGlobal(metaclass=Singtools):
    def __init__(self, app=None):
        self._app = app


class BaseManager(metaclass=Singtools):
    def getApp(self):
        return ManagerGlobal()._app


class ManagerFile(BaseManager):

    def open(self, path, mode="r", encoding="utf-8", new_line="\n", external=True):
        return open(path, mode, encoding=encoding, newline=new_line)

    def delete(self, path):
        os.remove(path)


class ManagerFolder:
    pass
