import abc
import asyncio as aio
import io

from java.io import BufferedReader, InputStreamReader, OutputStreamWriter
from java.util import Objects


class HandlerFileDialog(abc.ABC):
    """An abstract class that handles file manager calls"""

    def __init__(self, parent, app_toga):
        self.parent = parent
        self.app = app_toga._impl
        self.mActive = app_toga._impl.native

    @abc.abstractmethod
    def show(self):
        """Запуск менеджера"""
        pass


class BasePath(io.TextIOBase, abc.ABC):
    modes = []

    def __init__(self, app, stream):
        self.aloop: aio.AbstractEventLoop = app.loop
        self._stream = stream
        self._buffer = None
        self._is_binary = False
        self._new_line_int = 10
        self._encoding = "utf-8"

    def check_open(self):
        """The defense mechanism on the open is that path"""
        if self._buffer is None:
            raise TypeError("File not open!")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self._stream.close()
        if self._buffer is not None:
            self._buffer.close()

    @abc.abstractmethod
    def open(self, mode, encoding="utf-8", new_line="\n"):
        """Method for opening a file by path"""
        self._encoding = encoding
        self._new_line_int = new_line.encode(encoding)[0]
        if mode not in self.modes:
            raise ValueError(
                f"invalid mode {mode}.\nIt is allowed to use the following modes: R or RB"
            )
        if "b" in mode:
            self._is_binary = True


class BasePathReader(BasePath, abc.ABC):
    modes = ["r", "rb"]

    def open(self, mode="r", encoding="utf-8", new_line="\n"):
        """A method for opening a file for reading along the path"""
        super().open(mode.lower(), encoding, new_line)
        input_stream_reader = InputStreamReader(Objects.requireNonNull(self._stream))
        self._buffer = BufferedReader(input_stream_reader)

    @abc.abstractmethod
    def read(self, size=0):
        pass

    @abc.abstractmethod
    def readline(self, size=0):
        pass

    @abc.abstractmethod
    def aread(self, size=0):
        pass

    @abc.abstractmethod
    def areadline(self, size=0):
        pass


class PathReader(BasePathReader):
    """A file-like object for reading the contents of an android external storage file"""

    def readline(self, size: int = 0) -> str | bytes:
        """A function for reading lines from a file separated by new_line
        :param size: the number of rows to be counted.(Currently not implemented, added for future implementation)
        :return: Data type str[bytes](Depends on whether the flag and was passed) or the list of str[bytes]
        """
        self.check_open()
        res = bytearray()
        counter = size if size else "-1"
        while counter:
            resp: int = self._buffer.read()
            if resp == -1:
                break
            if resp == self._new_line_int:
                break
            res.append(resp)
            if isinstance(counter, int):
                counter -= 1
        if self._is_binary:
            return bytes(res)
        return res.decode(self._encoding)

    def read(self, size: int = 0) -> bytes | str:
        """A function for reading a string
        :param size: the number of characters to be counted. If it is equal to 0, the entire file will be read
        :return: Data type str[bytes](depends on whether the 'b' flag was passed)"""
        self.check_open()
        res = bytearray()
        counter = size if size else "-1"
        while counter:
            resp: int = self._buffer.read()
            if resp == -1:
                break
            res.append(resp)
            if isinstance(counter, int):
                counter -= 1
        if self._is_binary:
            return bytes(res)
        return res.decode(self._encoding)

    async def aread(self, size=0):
        """A function for reading a string
        :param size: the number of characters to be counted. If it is equal to 0, the entire file will be read
        :return: Data type str[bytes](depends on whether the 'b' flag was passed)"""
        self.check_open()
        res = bytearray()
        counter = size if size else "-1"
        while counter:
            resp: int = await self.aloop.run_in_executor(None, self._buffer.read)
            if resp == -1:
                break
            res.append(resp)
            if isinstance(counter, int):
                counter -= 1
        if self._is_binary:
            return bytes(res)
        return res.decode(self._encoding)

    def areadline(self, size=0):
        return NotImplemented


class BasePathWriter(BasePath, abc.ABC):
    modes = ["w", "wb"]

    def open(self, mode="r", encoding="utf-8", new_line="\n"):
        """A method for opening a file for writing along the path"""
        super().open(mode.lower(), encoding, new_line)
        self._buffer = OutputStreamWriter(self._stream)

    def _convertion_type_data(self, data):
        if isinstance(data, bytes) and not self._is_binary:
            return data.decode(self._encoding)
        if isinstance(data, str) and self._is_binary:
            return data.encode(self._encoding)
        return data

    @abc.abstractmethod
    def write(self, text: str | bytes):
        data = self._convertion_type_data(text)
        self._buffer.write(data)

    @abc.abstractmethod
    def awrite(self, text):
        pass


class PathWriter(BasePathReader):
    pass
