from __future__ import print_function, unicode_literals, absolute_import, division

import importlib
import os
import sys

from .constants import *

__all__ = [
    '__version__',
    'platform'
]

# Examples of valid version strings
# __version__ = '1.2.3.dev1'  # Development release 1
# __version__ = '1.2.3a1'     # Alpha Release 1
# __version__ = '1.2.3b1'     # Beta Release 1
# __version__ = '1.2.3rc1'    # RC Release 1
# __version__ = '1.2.3'       # Final Release
# __version__ = '1.2.3.post1' # Post Release 1

__version__ = '0.1.2'

platform = None


def set_platform(module_name=None, locals=locals()):
    "Configures toga to use the specfied platform module"
    # Note - locals is deliberately passed in as an argument; because it is
    # a dictionary, this results in the module level locals dictionary being
    # bound as a local variable in this method -- and a persistent one,
    # because it was evaluated and bound at time of method import.

    # First check for an environment variable setting the platform
    if module_name is None:
        module_name = os.environ.get('TOGA_PLATFORM')

    # If we don't have a manually defined platform, attempt to
    # autodetect and set the platform
    if module_name is None:
        if sys.platform == 'darwin':
            if os.environ.get('TARGET_IPHONE_SIMULATOR') or os.environ.get('TARGET_IPHONE'):
                module_name = 'toga_iOS'
            else:
                module_name = 'toga_cocoa'
        elif sys.platform in ('linux', 'linux2'):
            module_name = 'toga_gtk'
        elif sys.platform == 'win32':
            module_name = 'toga_win32'
        else:
            raise RuntimeError("Couldn't identify a supported host platform.")

    # Purge any existing platform symbols in the toga module
    if locals['platform']:
        for symbol in locals['platform'].__all__:
            # Exclude __version__ from the list of symbols that is
            # ported, because toga itself has a __version__ identifier.
            if symbol != '__version__':
                locals.pop(symbol)

    # Import the new platform module
    try:
        # Set the new platform module into the module namespace
        locals['platform'] = importlib.import_module(module_name)

        # Export all the symbols *except* for __version__ from the platform module
        # The platform has it's own version identifier.
        locals.update(dict(
            (symbol, getattr(platform, symbol))
            for symbol in locals['platform'].__all__
            if symbol != '__version__'
        ))
    except ImportError:
        locals['platform'] = None
        raise RuntimeError("Couldn't find %s platform module; try running 'pip install %s'." % (module_name, module_name))

# On first import, do an autodetection of platform.
set_platform()
