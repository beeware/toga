import abc
import io

import java

BufferedReader = java.jclass("java.io.BufferedReader")
InputStreamReader = java.jclass("java.io.InputStreamReader")
Objects = java.jclass("java.util.Objects")


class HandlerFileDialog(abc.ABC):
    """Абстрактный класс вызова файлового менеджера"""

    def __init__(self, parent, app_toga):
        self.parent = parent
        self.app = app_toga._impl
        self.mActive = app_toga._impl.native

    @abc.abstractmethod
    def show(self):
        """Запуск менеджера"""
        pass


class VFile(io.TextIOBase):
    """Файл для работы с внешнем хранилищем андроида"""

    def __init__(self, bufferedReader):
        self._bfr = bufferedReader

    def __del__(self):
        self.close()

    def close(self):
        self._bfr.close()

    def readline(self, size: int = 0) -> str:
        """Функция для чтения строки
        :param size: количество строк, которые нужно считать.
        Если он равен 0, то будет прочтен весь файл
        :return: Строка"""
        return self._bfr.readLine()

    def read(self, size: int = 0) -> str:
        """Функция для чтения строки
        :param size: количество символов, которые нужно считать.
        Если он равен 0, то будет прочтен весь файл
        :return: Строка"""
        res = ""
        counter = size if size else "+"
        while counter:
            resp = self._bfr.read()
            if resp == -1:
                break
            res += chr(resp)
            if isinstance(counter, int):
                counter -= 1
        return res
