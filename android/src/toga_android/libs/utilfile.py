import io
import abc
import java

BufferedReader = java.jclass("java.io.BufferedReader")
InputStreamReader = java.jclass("java.io.InputStreamReader")
Objects = java.jclass("java.util.Objects")


class HandlerFileDialog(abc.ABC):
    def __init__(self, parent, app_toga):
        self.parent = parent
        self.app = app_toga._impl
        self.mActive = app_toga._impl.native

    @abc.abstractmethod
    def show(self):
        pass


class VFile(io.TextIOBase):  #VirtualFile
    def __init__(self, bufferedReader):
        self._bfr = bufferedReader

    def __del__(self):
        self.close()

    def close(self):
        self._bfr.close()

    def readline(self, size=0):
        return self._bfr.readLine()

    def read(self, size=0):
        res = ""
        counter = size if size else "+"
        while counter:
            resp = self._bfr.read()
            if resp == -1: break
            res += chr(resp)
            if isinstance(counter, int):
                counter -= 1
        return res
