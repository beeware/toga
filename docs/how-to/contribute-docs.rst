=================================
Contributing to the documentation
=================================

Here are some tips for working on this documentation. You're welcome to add
more and help us out!

First of all, you should check the `Restructured Text (reST) and Sphinx
CheatSheet <http://thomas-cokelaer.info/tutorials/sphinx/rest_syntax.html>`_ to
learn how to write your .rst file.

Create a .rst file
---------------------

Look at the structure and choose the best category to put your .rst file. Make
sure that it is referenced in the index of the corresponding category, so it
will show on in the documentation. If you have no idea how to do this, study
the other index files for clues.

Build documentation locally
---------------------------

To build the documentation locally, :ref:`set up a development environment
<setup-dev-environment>`, and run:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ tox -e docs

  .. group-tab:: Linux

    .. code-block:: bash

      (venv) $ tox -e docs

  .. group-tab:: Windows

    .. code-block:: bash

      C:\...>tox -e docs

The output of the build should be in the ``docs/_build`` folder. If there
are any markup problems, they'll raise an error.
