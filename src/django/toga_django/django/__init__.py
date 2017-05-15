import importlib
import os

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class App(AppConfig):
    name = 'toga'
    label = 'toga'
    verbose_name = _("Toga")
    path = os.path.dirname(__file__)


def TogaApp(module_name):
    module = importlib.import_module(module_name + ".app")
    app = module.main()
    app._module = module
    return app

