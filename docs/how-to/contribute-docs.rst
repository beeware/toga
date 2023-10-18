====================================
Contributing to Toga's documentation
====================================

You might have the best software in the world - but if nobody knows how to use
it, what's the point? Documentation can always be improved - and we need need
your help!

Toga's documentation is written using `Sphinx and reStructuredText
<https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`__. We
aim to follow the `Diataxis <https://diataxis.fr>`__ framework for structuring
documentation.

Building Toga's documentation
=============================

To build Toga's documentation, start by :ref:`setting up a development
environment <setup-dev-environment>`.

You'll also need to install the Enchant spell checking library.

.. tabs::

  .. group-tab:: macOS

    Enchant can be installed using `Homebrew <https://brew.sh>`__:

    .. code-block:: console

      (venv) $ brew install enchant

    If you're on an M1 machine, you'll also need to manually set the location
    of the Enchant library:

    .. code-block:: console

      (venv) $ export PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.2.dylib

  .. group-tab:: Linux

    Enchant can be installed as a system package:

    **Ubuntu 20.04+ / Debian 10+**

    .. code-block:: console

      $ sudo apt update
      $ sudo apt install enchant-2

    **Fedora**

    .. code-block:: console

      $ sudo dnf install enchant

    **Arch, Manjaro**

    .. code-block:: console

      $ sudo pacman -Syu enchant

  .. group-tab:: Windows

    Enchant is installed automatically when you set up your development
    environment.

Build documentation locally
---------------------------

Once your development environment is set up, run:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ tox -e docs

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ tox -e docs

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>tox -e docs

The output of the file should be in the ``docs/_build/html`` folder. If there
are any markup problems, they'll raise an error.

Documentation linting
---------------------

The build process will identify reStructuredText problems, but Toga performs some
additional "lint" checks. To run the lint checks:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ tox -e docs-lint

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ tox -e docs-lint

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>tox -e docs-lint

This will validate the documentation does not contain:

* dead hyperlinks
* misspelled words

If a valid spelling of a word is identified as misspelled, then add the word to
the list in ``docs/spelling_wordlist``. This will add the word to the
spellchecker's dictionary. When adding to this list, remember:

* We prefer US spelling, with some liberties for programming-specific
  colloquialism (e.g., "apps") and verbing of nouns (e.g., "scrollable")
* Any reference to a product name should use the product's preferred
  capitalization. (e.g., "macOS", "GTK", "pytest", "Pygame", "PyScript").
* If a term is being used "as code", then it should be quoted as a literal
  rather than being added to the dictionary.

Rebuilding all documentation
----------------------------

To force a rebuild for all of the documentation:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ tox -e docs-all

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ tox -e docs-all

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>tox -e docs-all

The documentation should be fully rebuilt in the ``docs/_build/html`` folder.
If there are any markup problems, they'll raise an error.

What to work on?
================

If you're looking for specific areas to improve, there are `tickets tagged
"documentation"
<https://github.com/beeware/toga/issues?q=is%3Aopen+is%3Aissue+label%3Adocumentation>`__
in Toga's issue tracker.

However, you don't need to be constrained by these tickets. If you can identify
a gap in Toga's documentation, or an improvement that can be made, start
writing! Anything that improves the experience of the end user is a welcome
change.

Submitting a pull request
=========================

Before you submit a pull request, there's a few bits of housekeeping to do. See the
section on submitting a pull request in the :ref:`code contribution guide
<pr-housekeeping>` for details on our submission process.
