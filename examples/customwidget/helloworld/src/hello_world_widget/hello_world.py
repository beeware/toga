from functools import cached_property

from toga import Widget
from toga.platform import get_factory


class HelloWorld(Widget):
    @cached_property
    def factory(self):
        return get_factory("togax_hello_world")

    def _create(self):
        return self.factory.HelloWorld(interface=self)
