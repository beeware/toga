=======
Testing
=======

Toga provides a `toga-dummy <https://github.com/beeware/toga/tree/main/dummy>`__ backend
that can be used for testing purposes. This backend implements the full interface
required by a platform backend, but does not display any widgets visually. It provides
an API that can be used to verify widget operation.

Prerequisites
-------------

The dummy backend has no prerequisites.

Installation
------------

The dummy backend must be installed manually:

.. code-block:: console

    $ python -m pip install toga-dummy

To force Toga to use the dummy backend, it must either be the only backend that is
installed in the current Python environment, or you must define the ``TOGA_BACKEND``
environment variable:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ export TOGA_BACKEND=toga_dummy

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ export TOGA_BACKEND=toga_dummy

  .. group-tab:: Windows

    .. code-block:: console

      (venv) $ set TOGA_BACKEND=toga_dummy
