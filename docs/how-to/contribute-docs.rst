Contributing to the documentation
=================================

Here are some tips for working on this documentation. You're welcome to add
more and help us out!

First of all, you should check the `Restructured Text (reST) and Sphinx
CheatSheet <http://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_ to
learn how to write your ``.rst`` file.

Create a ``.rst`` file
----------------------

Look at the structure and choose the best category to put your ``.rst`` file. Make
sure that it is referenced in the index of the corresponding category, so it
will show on in the documentation. If you have no idea how to do this, study
the other index files for clues.

Build documentation locally
---------------------------

To build the documentation locally, :ref:`set up a development environment
<setup-dev-environment>`.

You'll also need to install the Enchant spell checking library.

.. tabs::

  .. group-tab:: macOS

    Enchant can be installed using `Homebrew <https://brew.sh>`__:

    .. code-block:: bash

      (venv) $ brew install enchant

    If you're on an M1 machine, you'll also need to manually set the location
    of the Enchant library:

    .. code-block:: bash

      (venv) $ export PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.2.dylib

  .. group-tab:: Linux

    Enchant can be installed as a system package:

    **Ubuntu 20.04+ / Debian 10+**

    .. code-block:: console

      $ sudo apt-get update
      $ sudo apt-get install enchant-2

    **Fedora**

    .. code-block:: console

      $ sudo dnf install enchant

    **Arch, Manjaro**

    .. code-block:: console

      $ sudo pacman -Syu enchant

  .. group-tab:: Windows

    Enchant is installed automatically when you set up your development
    environment.

Once your development environment is set up, run:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ tox -e docs

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ tox -e docs

  .. group-tab:: Windows

    .. code-block:: powershell

      (venv) C:\...>tox -e docs

The output of the file should be in the ``docs/_build/html`` folder. If there
are any markup problems, they'll raise an error.

Documentation linting
---------------------

Before committing and pushing documentation updates, run linting for the
documentation:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ tox -e docs-lint

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ tox -e docs-lint

  .. group-tab:: Windows

    .. code-block:: powershell

      (venv) C:\...>tox -e docs-lint

This will validate the documentation does not contain:

* invalid syntax and markup
* dead hyperlinks
* misspelled words

If a valid spelling of a word is identified as misspelled, then add the word to
the list in ``docs/spelling_wordlist``. This will add the word to the
spellchecker's dictionary.

If you get an error related to SSL certificate verification::

    Exception occurred:
      File "/Library/Frameworks/Python.framework/Versions/3.10/lib/python3.10/ssl.py", line 1342, in do_handshake
        self._sslobj.do_handshake()
    ssl.SSLCertVerificationError: [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify failed: unable to get local issuer certificate (_ssl.c:1007)

The root certificate on your machine is out of date. You can correct this by
installing the Python package `certifi`, and using that package to provide your
SSL root certificate:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ python -m pip install certifi
      (venv) $ export SSL_CERT_FILE=$(python -m certifi)

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ python -m pip install certifi
      (venv) $ export SSL_CERT_FILE=$(python -m certifi)

  .. group-tab:: Windows

    .. code-block:: powershell

      (venv) C:\...>python -m pip install certifi
      (venv) C:\...>FOR /f "delims=" %i IN ('python -m certifi') DO SET SSL_CERT_FILE=%i

Rebuilding all documentation
----------------------------

To force a rebuild for all of the documentation:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ tox -e docs-all

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ tox -e docs-all

  .. group-tab:: Windows

    .. code-block:: powershell

      (venv) C:\...>tox -e docs-all

The documentation should be fully rebuilt in the ``docs/_build/html`` folder.
If there are any markup problems, they'll raise an error.
