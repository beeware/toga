import importlib
import os
import sys
import types

from .constants import *

# Work around import loop issues (toga -> platform -> toga.interface) import
# all these things before we import the platform stuff
import toga.interface.app  # NOQA

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

__version__ = '0.2.8'

platform = None


def get_platform_name():
    """
    Get the name of the current platform
    :return: The name of the platform, e.g. tvOS
    :rtype: ``str``
    """
    platform_name = os.environ.get('TOGA_PLATFORM')

    # If we don't have a manually defined platform, attempt to
    # autodetect and set the platform
    if platform_name is None:
        if sys.platform == 'ios':
            platform_name = 'iOS'
        elif sys.platform == 'tvos':
            platform_name = 'tvOS'
        elif sys.platform == 'watchos':
            platform_name = 'watchOS'
        elif sys.platform == 'android':
            platform_name = 'android'
        elif sys.platform == 'darwin':
            platform_name = 'cocoa'
        elif sys.platform == 'linux':
            platform_name = 'gtk'
        elif sys.platform == 'win32':
            platform_name = 'winforms'
        else:
            raise RuntimeError("Couldn't identify a supported host platform.")
    return platform_name


def set_platform(module_name=None, local_vars=locals()):
    "Configures toga to use the specified platform module"
    # Note - locals is deliberately passed in as an argument; because it is
    # a dictionary, this results in the module level locals dictionary being
    # bound as a local variable in this method -- and a persistent one,
    # because it was evaluated and bound at time of method import.

    # First check for an environment variable setting the platform
    if module_name is None:
        platform_name = get_platform_name()
        module_name = 'toga_' + platform_name

    # # Purge any existing platform symbols in the toga module
    # if local_vars['platform']:
    #     for symbol in local_vars['platform'].__all__:
    #         # Exclude __version__ from the list of symbols that is
    #         # ported, because toga itself has a __version__ identifier.
    #         if symbol != '__version__':
    #             # Remove any modules from the importable module list
    #             if isinstance(local_vars[symbol], types.ModuleType):
    #                 del sys.modules['toga.%s' % symbol]
    #             local_vars.pop(symbol)

    # Import the new platform module
    try:
        # Set the new platform module into the module namespace
        local_vars['platform'] = importlib.import_module(module_name)

        # Export all the symbols *except* for __version__ from the platform module
        # The platform has it's own version identifier.
        for symbol in local_vars['platform'].__all__:
            if symbol == '__version__':
                if local_vars['platform'].__version__ != __version__:
                    raise RuntimeError('Toga core is version %s; %s platform backend is version %s.' % (
                            __version__,
                            module_name,
                            local_vars['platform'].__version__
                        )
                    )
            else:
                local_vars[symbol] = getattr(local_vars['platform'], symbol)
                # Make sure any modules are added to the importable module list
                if isinstance(local_vars[symbol], types.ModuleType):
                    sys.modules['toga.%s' % symbol] = local_vars[symbol]
    except ImportError as e:
        if e.name == module_name:
            local_vars['platform'] = None
            print("Couldn't import %s platform module; try running 'pip install %s'." % (module_name[5:], module_name))
            sys.exit(-1)
        else:
            raise

# On first import, do an auto-detection of platform.
if get_platform_name() != 'dummy':
    set_platform()
