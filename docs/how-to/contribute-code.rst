.. _contribute:

==============================
How to contribute code to Toga
==============================

If you experience problems with Toga, `log them on GitHub`_. If you want to
contribute code, please `fork the code`_ and `submit a pull request`_.  You may
also find `this presentation by BeeWare team member Dan Yeaw
<https://youtu.be/sWt_sEZUiY8>`__ helpful. This talk gives an architectural
overview of Toga, as well as providing a guide to the process of adding new
widgets.

.. _log them on Github: https://github.com/beeware/toga/issues
.. _fork the code: https://github.com/beeware/toga
.. _submit a pull request: https://github.com/beeware/toga/pulls

.. _setup-dev-environment:

Set up your development environment
===================================

First thing is to ensure that you have Python 3 and pip installed. To do this run the following commands:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      $ python3 --version
      $ pip3 --version

  .. group-tab:: Unix-like

    .. code-block:: bash

      $ python3 --version
      $ pip3 --version

  .. group-tab:: Windows

    .. code-block:: doscon

      C:\...>python3 --version
      C:\...>pip3 --version

The recommended way of setting up your development environment for Toga
is to install a virtual environment, install the required dependencies and
start coding. To set up a virtual environment, run:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      $ python3 -m venv venv
      $ source venv/bin/activate

  .. group-tab:: Unix-like

    .. code-block:: bash

      $ python3 -m venv venv
      $ source venv/bin/activate

  .. group-tab:: Windows

    .. code-block:: doscon

      C:\...>python3 -m venv venv
      C:\...>venv/Scripts/activate

Your prompt should now have a ``(venv)`` prefix in front of it.

Next, install any additional dependencies for your operating system:

.. tabs::

  .. group-tab:: macOS

    No additional dependencies

  .. group-tab:: Unix-like

    .. code-block:: bash

      # Freebsd13
      (venv) $ sudo pkg update
      (venv) $ sudo pkg install gtk3 gobject-introspection cairo webkit2-gtk3

      # Ubuntu 16.04, Debian 9
      (venv) $ sudo apt-get update
      (venv) $ sudo apt-get install python3-dev libgirepository1.0-dev libcairo2-dev libpango1.0-dev libwebkitgtk-3.0-0 gir1.2-webkit-3.0

      # Ubuntu 20.04, Ubuntu 18.04, Debian 10
      (venv) $ sudo apt-get update
      (venv) $ sudo apt-get install python3-dev libgirepository1.0-dev libcairo2-dev libpango1.0-dev libwebkit2gtk-4.0-37 gir1.2-webkit2-4.0

      # Fedora
      (venv) $ sudo dnf install pkg-config python3-devel gobject-introspection-devel cairo-devel cairo-gobject-devel pango-devel webkitgtk3

  .. group-tab:: Windows

    No additional dependencies

Next, go to `the Toga page on Github <https://github.com/beeware/toga>`__, and
fork the repository into your own account, and then clone a copy of that
repository onto your computer by clicking on "Clone or Download". If you
have the Github desktop application installed on your computer, you can
select "Open in Desktop"; otherwise, copy the URL provided, and use it
to clone using the command line:

.. tabs::

  .. group-tab:: macOS

    Fork the Toga repository, and then::

      (venv) $ git clone https://github.com/<your username>/toga.git

    (substituting your Github username)

  .. group-tab:: Unix-like

    Fork the Toga repository, and then::

      (venv) $ git clone https://github.com/<your username>/toga.git

    (substituting your Github username)

  .. group-tab:: Windows

    Fork the Toga repository, and then:

    .. code-block:: doscon

      (venv) C:\...>git clone https://github.com/<your username>/toga.git

    (substituting your Github username)

Now that you have the source code, you can install Toga into your development
environment. The Toga source repository contains multiple packages. Since
we're installing from source, we can't rely on pip to install the packages in
dependency order. Therefore, we have to manually install each package in a
specific order:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ cd toga
      (venv) $ pip install -e ./core[dev]
      (venv) $ pip install -e ./dummy
      (venv) $ pip install -e ./cocoa

  .. group-tab:: Unix-like

    .. code-block:: bash

      (venv) $ cd toga
      (venv) $ pip install -e ./core[dev]
      (venv) $ pip install -e ./dummy
      (venv) $ pip install -e ./gtk

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>cd toga
      (venv) C:\...>pip install -e ./core[dev]
      (venv) C:\...>pip install -e ./dummy
      (venv) C:\...>pip install -e ./winforms

This project uses a tool called `Pre-Commit <https://pre-commit.com>`__ to identify
simple issues and standardize code formatting. It does this by installing a git
hook that automatically runs a series of code linters prior to finalizing any
git commit. To enable pre-commit, run:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ pre-commit install
      pre-commit installed at .git/hooks/pre-commit

  .. group-tab:: Unix-like

    .. code-block:: bash

      (venv) $ pre-commit install
      pre-commit installed at .git/hooks/pre-commit

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>pre-commit install
      pre-commit installed at .git/hooks/pre-commit

When you commit any change, pre-commit will run automatically. If there are any
issues found with the commit, this will cause your commit to fail. Where possible,
pre-commit will make the changes needed to correct the problems it has found:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ git add some/interesting_file.py
      (venv) $ git commit -m "Minor change"
      black....................................................................Failed
      - hook id: black
      - files were modified by this hook

      reformatted some/interesting_file.py

      All done! ✨ 🍰 ✨
      1 file reformatted.

      flake8...................................................................Passed
      check toml...........................................(no files to check)Skipped
      check yaml...........................................(no files to check)Skipped
      check for case conflicts.................................................Passed
      check docstring is first.................................................Passed
      fix end of files.........................................................Passed
      trim trailing whitespace.................................................Passed
      isort....................................................................Passed
      pyupgrade................................................................Passed
      docformatter.............................................................Passed

  .. group-tab:: Unix-like

    .. code-block:: bash

      (venv) $ git add some/interesting_file.py
      (venv) $ git commit -m "Minor change"
      black....................................................................Failed
      - hook id: black
      - files were modified by this hook

      reformatted some/interesting_file.py

      All done! ✨ 🍰 ✨
      1 file reformatted.

      flake8...................................................................Passed
      check toml...........................................(no files to check)Skipped
      check yaml...........................................(no files to check)Skipped
      check for case conflicts.................................................Passed
      check docstring is first.................................................Passed
      fix end of files.........................................................Passed
      trim trailing whitespace.................................................Passed
      isort....................................................................Passed
      pyupgrade................................................................Passed
      docformatter.............................................................Passed

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>git add some/interesting_file.py
      (venv) C:\...>git commit -m "Minor change"
      black....................................................................Failed
      - hook id: black
      - files were modified by this hook

      reformatted some\interesting_file.py

      All done! ✨ 🍰 ✨
      1 file reformatted.

      flake8...................................................................Passed
      check toml...........................................(no files to check)Skipped
      check yaml...........................................(no files to check)Skipped
      check for case conflicts.................................................Passed
      check docstring is first.................................................Passed
      fix end of files.........................................................Passed
      trim trailing whitespace.................................................Passed
      isort....................................................................Passed
      pyupgrade................................................................Passed
      docformatter.............................................................Passed

You can then re-add any files that were modified as a result of the pre-commit checks,
and re-commit the change.

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ git add some/interesting_file.py
      (venv) $ git commit -m "Minor change"
      black....................................................................Passed
      flake8...................................................................Passed
      check toml...........................................(no files to check)Skipped
      check yaml...........................................(no files to check)Skipped
      check for case conflicts.................................................Passed
      check docstring is first.................................................Passed
      fix end of files.........................................................Passed
      trim trailing whitespace.................................................Passed
      isort....................................................................Passed
      pyupgrade................................................................Passed
      docformatter.............................................................Passed
      [bugfix e3e0f73] Minor change
      1 file changed, 4 insertions(+), 2 deletions(-)

  .. group-tab:: Unix-like

    .. code-block:: bash

      (venv) $ git add some/interesting_file.py
      (venv) $ git commit -m "Minor change"
      black....................................................................Passed
      flake8...................................................................Passed
      check toml...........................................(no files to check)Skipped
      check yaml...........................................(no files to check)Skipped
      check for case conflicts.................................................Passed
      check docstring is first.................................................Passed
      fix end of files.........................................................Passed
      trim trailing whitespace.................................................Passed
      isort....................................................................Passed
      pyupgrade................................................................Passed
      docformatter.............................................................Passed
      [bugfix e3e0f73] Minor change
      1 file changed, 4 insertions(+), 2 deletions(-)

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>git add some\interesting_file.py
      (venv) C:\...>git commit -m "Minor change"
      black....................................................................Passed
      flake8...................................................................Passed
      check toml...........................................(no files to check)Skipped
      check yaml...........................................(no files to check)Skipped
      check for case conflicts.................................................Passed
      check docstring is first.................................................Passed
      fix end of files.........................................................Passed
      trim trailing whitespace.................................................Passed
      isort....................................................................Passed
      pyupgrade................................................................Passed
      docformatter.............................................................Passed

Now you are ready to start hacking on Toga!

What should I do?
=================

Start by running the core test suite. Toga uses
`tox <https://tox.readthedocs.io/en/latest/>`__ to manage the testing process.
To run the core test suite:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: bash

      (venv) $ tox -e py-core

  .. group-tab:: Unix-like

    .. code-block:: bash

      (venv) $ tox -e py-core

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>tox -e py-core

You should get some output indicating that tests have been run. You shouldn't
ever get any FAIL or ERROR test results. We run our full test suite before
merging every patch. If that process discovers any problems, we don't merge
the patch. If you do find a test error or failure, either there's something
odd in your test environment, or you've found an edge case that we haven't
seen before - either way, let us know!

Although the tests should all pass, the test suite itself is still
incomplete. There are many aspects of the Toga Core API that aren't currently
tested (or aren't tested thoroughly). To work out what *isn't* tested, we're
going to use a tool called `coverage
<http://coverage.readthedocs.io/en/coverage-4.4.1/>`__. Coverage allows you to
check which lines of code have (and haven't) been executed - which then gives
you an idea of what code has (and hasn't) been tested.

At the end of the test output there should be a report of the coverage data that
was gathered::

      Name                                 Stmts   Miss  Cover   Missing
      ------------------------------------------------------------------
      toga/__init__.py                        29      0   100%
      toga/app.py                             50      0   100%
      ...
      toga/window.py                          79     18    77%   58, 75, 87, 92, 104, 141, 155, 164, 168, 172-173, 176, 192, 204, 216, 228, 243, 257
      ------------------------------------------------------------------
      TOTAL                                 1034    258    75%

What does this all mean? Well, the "Cover" column tells you what proportion of
lines in a given file were executed during the test run. In this run, every
line of ``toga/app.py`` was executed; but only 77% of lines in
``toga/window.py`` were executed. Which lines were missed? They're listed in
the next column: lines 58, 75, 87, and so on weren't executed.

That's what you have to fix - ideally, every single line in every single file
will have 100% coverage. If you look in `core/tests`, you should find a
test file that matches the name of the file that has insufficient coverage. If
you don't, it's possible the entire test file is missing - so you'll have to
create it!

Your task: create a test that improves coverage - even by one more line.

Once you've written a test, re-run the test suite to generate fresh coverage
data. Let's say we added a test for line 58 of ``toga/window.py`` - we'd
expect to see something like::

      Name                                 Stmts   Miss  Cover   Missing
      ------------------------------------------------------------------
      toga/__init__.py                        29      0   100%
      toga/app.py                             50      0   100%
      ...
      toga/window.py                          79     17    78%   75, 87, 92, 104, 141, 155, 164, 168, 172-173, 176, 192, 204, 216, 228, 243, 257
      ------------------------------------------------------------------
      TOTAL                                 1034    257    75%

That is, one more test has been executed, resulting in one less missing line
in the coverage results.

Add change information for release notes
----------------------------------------

Before you submit this change as a pull request, there's one more thing
required. Toga uses `towncrier <https://pypi.org/project/towncrier/>`__ to
automate building release notes. To support this, every pull request needs to
have a corresponding file in the ``changes/`` directory that provides a short
description of the change implemented by the pull request.

This description should be a high level summary of the change from the
perspective of the user, not a deep technical description or implementation
detail. It is distinct from a commit message - a commit message describes
what has been done so that future developers can follow the reasoning for
a change; the change note is a "user facing" description. For example, if
you fix a bug caused by date handling, the commit message might read:

    Modified date validation to accept US-style MM-DD-YYYY format.

The corresponding change note would read something like:

    Date widgets can now accept US-style MM-DD-YYYY format.

See `News Fragments <https://pypi.org/project/towncrier/#news-fragments>`__
for more details on the types of news fragments you can add. You can also see
existing examples of news fragments in the ``changes/`` folder. Name the file
using the number of the issue that your pull request is addressing. When there
isn't an existing issue, you can create the pull request in two passes: First
submit it without a change note - this will fail, but will also assign a pull
request number. You can then push an update to the pull request, adding the
change note with the assigned number.

Once you've written your code, test, and change note, you can submit your
changes as a pull request. One of the core team will review your work, and
give feedback. If any changes are requested, you can make those changes, and
update your pull request; eventually, the pull request will be accepted and
merged. Congratulations, you're a contributor to Toga!

It's not just about coverage!
=============================

Although improving test coverage is the goal, the task ahead of you isn't
*just* about increasing numerical coverage. Part of the task is to audit the
code as you go. You could write a comprehensive set of tests for a concrete
life jacket... but a concrete life jacket would still be useless for the
purpose it was intended!

As you develop tests and improve coverage, you should be checking that the
core module is internally **consistent** as well. If you notice any method
names that aren't internally consistent (e.g., something called ``on_select``
in one module, but called ``on_selected`` in another), or where the data isn't
being handled consistently (one widget updates then refreshes, but another
widget refreshes then updates), flag it and bring it to our attention by
raising a ticket. Or, if you're confident that you know what needs to be done,
create a pull request that fixes the problem you've found.

One example of the type of consistency we're looking for is described in
`this ticket <https://github.com/beeware/toga/issues/299>`__.

What next?
==========

Rinse and repeat! Having improved coverage by one line, go back and do it
again for *another* coverage line!

If you're feeling particularly adventurous, you could start looking at a
specific platform backend. The Toga Dummy API defines the API that a backend
needs to implement; so find a platform backend of interest to you (e.g., cocoa
if you're on macOS), and look for a widget that isn't implemented (a missing
file in the ``widgets`` directory for that platform, or an API *on* a widget
that isn't implemented (these will be flagged by raising
``NotImplementedError()``). Dig into the documentation for native widgets for
that platform (e.g., the Apple Cocoa documentation), and work out how to map
native widget capabilities to the Toga API. You may find it helpful to look at
existing widgets to work out what is needed.

Most importantly - have fun!

Advanced Mode
=============

If you've got expertise in a particular platform (for example, if you've got
experience writing iOS apps), or you'd *like* to have that experience, you
might want to look into a more advanced problem. Here are some suggestions:

* **Implement a platform native widget** If the core library already specifies
  an interface, implement that interface; if no interface exists, propose an
  interface design, and implement it for at least one platform.

* **Add a new feature to an existing widget API** Can you think of a feature
  than an existing widget should have? Propose a new API for that widget, and
  provide a sample implementation.

* **Improve platform specific testing** The tests that have been described in
  this document are all platform independent. They use the dummy backend to
  validate that data is being passed around correctly, but they don't validate
  that on a given platform, widgets behave they way they should. If I put a
  button on a Toga app, is that button displayed? Is it in the right place? Does
  it respond to mouse clicks? Ideally, we'd have automated tests to validate
  these properties. However, automated tests of GUI operations can be difficult
  to set up. If you've got experience with automated GUI testing, we'd love to
  hear your suggestions.

* **Improve the testing API for application writers** The dummy backend exists
  to validate that Toga's internal API works as expected. However, we would like
  it to be a useful resource for *application* authors as well. Testing GUI
  applications is a difficult task; a Dummy backend would potentially allow an
  end user to write an application, and validate behavior by testing the
  properties of the Dummy. Think of it as a GUI mock - but one that is baked into
  Toga as a framework. See if you can write a GUI app of your own, and write
  a test suite that uses the Dummy backend to validate the behavior of that app.
