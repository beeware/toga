import abc
import asyncio as aio
import io
import os
from dataclasses import dataclass

from java.io import BufferedReader, InputStreamReader, OutputStreamWriter
from java.util import Objects

import toga


class BaseFile(io.TextIOBase):
    def __init__(self, stream, binary, encoding, newLineInt):
        self.aloop: aio.AbstractEventLoop = toga.App.app._impl.loop
        self._stream = stream
        self._buffer = None
        self._is_binary = binary
        self._new_line_int = newLineInt
        self._encoding = encoding

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


@dataclass
class BaseDataOpen:
    binary: bool
    encoding: str
    newLineInt: int


class BasePath(os.PathLike):
    modes = []

    def __init__(self, content, uri):
        self._uri = uri
        self._content = content
        self._stream = None

    @abc.abstractmethod
    def open(self, mode, encoding="utf-8", new_line="\n"):
        """Method for opening a file by path"""
        _new_line_int = new_line.encode(encoding)[0]
        if mode not in self.modes:
            raise ValueError(
                f"""invalid mode {mode}.
                It is allowed to use the following modes: R or RB"""
            )
        _is_binary = "b" in mode
        return BaseDataOpen(_is_binary, encoding, _new_line_int)


class BaseFileReader(BaseFile, abc.ABC):

    def __init__(self, stream, binary, encoding, newLineInt):
        super().__init__(stream, binary, encoding, newLineInt)
        input_stream_reader = InputStreamReader(Objects.requireNonNull(self._stream))
        self._buffer = BufferedReader(input_stream_reader)

    @abc.abstractmethod
    def read(self, size=0):
        pass

    @abc.abstractmethod
    def readline(self, size=0):
        pass

    @abc.abstractmethod
    async def aread(self, size=0):
        pass

    @abc.abstractmethod
    async def areadline(self, size=0):
        pass


class FileReader(BaseFileReader):
    """A phalloid object for reading.
    Reads the contents of the Android external storage file"""

    def readline(self, size: int = 0) -> str | bytes:
        """A function for reading lines from a file
        :param size: the number of rows to be counted.
        (Currently not implemented, added for future implementation)
        :return: Data type str[bytes]
        (Depends on whether the flag and was passed) or the list of str[bytes]
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
        :param size: the number of characters to be counted.
        If it is equal to 0, the entire file will be read
        :return: Data type str[bytes]
        (depends on whether the 'b' flag was passed)"""
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
        """Asynchronous function for reading a string
        :parameter size: the number of characters to count.
        If it is equal to 0, the entire file will be read
        :returns: data type str[bytes]
        (depends on whether the 'b' flag was passed)"""
        self.check_open()
        return await self.aloop.run_in_executor(None, self.read, size)

    async def areadline(self, size=0):
        """Asynchronous function for reading lines from a file
        : parameter size: the number of rows to count.
        (Currently not implemented, added for future implementation)
        :returns: data type str[byte]
        (Depends on whether and flag was passed) or the str[byte] list"""
        return await self.aloop.run_in_executor(None, self.readline, size)


class BaseFileWriter(BaseFile, abc.ABC):

    def __init__(self, stream, binary, encoding, newLineInt):
        super().__init__(stream, binary, encoding, newLineInt)
        self._buffer = OutputStreamWriter(self._stream)

    def _convertion_type_data(self, data):
        if isinstance(data, bytes) and not self._is_binary:
            return data.decode(self._encoding)
        if isinstance(data, str) and self._is_binary:
            return data.encode(self._encoding)
        return data

    @abc.abstractmethod
    def write(self, text: str | bytes):
        pass

    @abc.abstractmethod
    async def awrite(self, text):
        pass


class FileWriter(BaseFileWriter):
    def write(self, text: str | bytes):
        data = self._convertion_type_data(text)
        self._buffer.write(data)

    def awrite(self, text):
        pass


class Path(BasePath):
    modes = ["r", "rb", "w", "wb"]

    def open(self, mode="r", encoding="utf-8", new_line="\n"):
        """A method for opening a file for reading along the path"""
        dataOpen = super().open(mode.lower(), encoding, new_line)
        if "r" in mode.lower():
            self._stream = self._content.openInputStream(self._uri)
            return FileReader(
                self._stream, dataOpen.binary, dataOpen.encoding, dataOpen.newLineInt
            )
        if "w" in mode.lower():
            self._stream = self._content.openOutputStream(self._uri)
            return FileWriter(
                self._stream, dataOpen.binary, dataOpen.encoding, dataOpen.newLineInt
            )

    def __fspath__(self):
        return str(self._uri)
