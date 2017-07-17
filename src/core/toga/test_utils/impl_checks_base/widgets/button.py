from ..utils.base import ImplCheckMixin
from ..utils.ast_helper import DefinitionExtractor
from toga_dummy.widgets import button
import unittest


class TestButtonImpl(ImplCheckMixin, unittest.TestCase):
    PATH_DUMMY = button.__file__
