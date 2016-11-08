import os

from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class TogaApp(AppConfig):
    name = 'toga'
    label = 'toga'
    verbose_name = _("Toga")
    path = os.path.dirname(__file__)
