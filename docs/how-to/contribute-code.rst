.. _contribute:

==============================
How to contribute code to Toga
==============================

If you experience problems with Toga, `log them on GitHub`_. If you want to
contribute code, please `fork the code`_ and `submit a pull request`_.

.. _log them on GitHub: https://github.com/beeware/toga/issues
.. _fork the code: https://github.com/beeware/toga
.. _submit a pull request: https://github.com/beeware/toga/pulls

.. _setup-dev-environment:

Set up your development environment
===================================

First, ensure that you have Python 3 and pip installed. To do this, run:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      $ python3 --version
      $ pip3 --version

  .. group-tab:: Linux

    .. code-block:: console

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

    .. code-block:: console

      $ python3 -m venv venv
      $ source venv/bin/activate

  .. group-tab:: Linux

    .. code-block:: console

      $ python3 -m venv venv
      $ source venv/bin/activate

  .. group-tab:: Windows

    .. code-block:: doscon

      C:\...>python3 -m venv venv
      C:\...>venv\Scripts\activate

Your prompt should now have a ``(venv)`` prefix in front of it.

Next, install any additional dependencies for your operating system:

.. tabs::

  .. group-tab:: macOS

    No additional dependencies

  .. group-tab:: Linux

    Ubuntu 18.04+, Debian 10+

    .. code-block:: console

      (venv) $ sudo apt update
      (venv) $ sudo apt install pkg-config python3-dev libgirepository1.0-dev libcairo2-dev gir1.2-webkit2-4.0 libcanberra-gtk3-module

    Fedora

    .. code-block:: console

      (venv) $ sudo dnf install pkg-config python3-devel gobject-introspection-devel cairo-gobject-devel webkit2gtk3 libcanberra-gtk3

    Arch / Manjaro

    .. code-block:: console

      (venv) $ sudo pacman -Syu git pkgconf gobject-introspection cairo webkit2gtk libcanberra

    FreeBSD

    .. code-block:: console

      (venv) $ sudo pkg update
      (venv) $ sudo pkg install gobject-introspection cairo webkit2-gtk3

  .. group-tab:: Windows

    No additional dependencies

Next, go to `the Toga page on GitHub <https://github.com/beeware/toga>`__, fork
the repository into your own account, and then clone a copy of that repository
onto your computer by clicking on "Clone or Download". If you have the GitHub
desktop application installed on your computer, you can select "Open in
Desktop"; otherwise, copy the URL provided, and use it to clone using the
command line:

.. tabs::

  .. group-tab:: macOS

    Fork the Toga repository, and then::

      (venv) $ git clone https://github.com/<your username>/toga.git

    (substituting your GitHub username)

  .. group-tab:: Linux

    Fork the Toga repository, and then::

      (venv) $ git clone https://github.com/<your username>/toga.git

    (substituting your GitHub username)

  .. group-tab:: Windows

    Fork the Toga repository, and then:

    .. code-block:: doscon

      (venv) C:\...>git clone https://github.com/<your username>/toga.git

    (substituting your GitHub username)

Now that you have the source code, you can install Toga into your development
environment. The Toga source repository contains multiple packages. Since we're
installing from source, we can't rely on pip to resolve the dependencies to
source packages, so we have to manually install each package:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ cd toga
      (venv) $ pip install -e "./core[dev]" -e ./dummy -e ./cocoa

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ cd toga
      (venv) $ pip install -e ./core[dev] -e ./dummy -e ./gtk

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>cd toga
      (venv) C:\...>pip install -e ./core[dev] -e ./dummy -e ./winforms

Toga uses a tool called `Pre-Commit <https://pre-commit.com>`__ to identify
simple issues and standardize code formatting. It does this by installing a git
hook that automatically runs a series of code linters prior to finalizing any
git commit. To enable pre-commit, run:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ pre-commit install
      pre-commit installed at .git/hooks/pre-commit

  .. group-tab:: Linux

    .. code-block:: console

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

    .. code-block:: console

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

  .. group-tab:: Linux

    .. code-block:: console

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

    .. code-block:: console

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

  .. group-tab:: Linux

    .. code-block:: console

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

Depending on your level of expertise, or areas of interest, there are a number
of ways you can contribute to Toga's code.

Fix a bug in an existing widget
-------------------------------

Toga's issue tracker logs the `known issues with existing widgets
<https://github.com/beeware/toga/issues?q=is%3Aopen+is%3Aissue+label%3Abug>`__.
Any of these issues are candidates to be worked on. This list can be filtered by
platform, so you can focus on issues that affect the platforms you're able to
test on. There's also a filter for `good first issues
<https://github.com/beeware/toga/issues?q=is%3Aopen+is%3Aissue+label%3A%22good+first+issue%22>`__
. These have been identified as problems that have a known cause, and we believe
the fix *should* be relatively simple (although we might be wrong in our
analysis).

We don't have any formal process of "claiming" or "assigning" issues; if you're
interested in a ticket, leave a comment that says you're working on it. If
there's an existing comment that says someone is working on the issue, and that
comment is recent, then leave a comment asking if they're still working on the
issue. If you don't get a response in a day or two, you can assume the issue is
available. If the most recent comment is more than a few weeks old, it's
probably safe to assume that the issue is still available to be worked on.

If an issue is particularly old (more than 6 months), it's entirely possible
that the issue has been resolved, so the first step is to verify that you can
reproduce the problem. Use the information provided in the bug report to try and
reproduce the problem. If you can't reproduce the problem, report what you have
found as a comment on the ticket, and pick another ticket.

If a bug report has no comments from anyone other than the original reporter,
the issue needs to be triaged. Triaging a bug involves taking the
information provided by the reporter, and trying to reproduce it. Again, if you
can't reproduce the problem, report what you have found as a comment on the
ticket, and pick another ticket.

If you can reproduce the problem - try to fix it! Work out what combination of core and
backend-specific code is implementing the feature, and see if you can work out what
isn't working correctly. You may need to refer to platform specific documentation (e.g.,
the `Cocoa AppKit <https://developer.apple.com/documentation/appkit?language=objc>`__,
`iOS UIKit <https://developer.apple.com/documentation/uikit?language=objc>`__, `GTK
<https://docs.gtk.org/gtk3/>`__, `Winforms
<https://learn.microsoft.com/en-us/dotnet/desktop/winforms/controls/overview?view=netdesktop-7.0>`__,
`Android <https://developer.android.com/reference>`__, `Shoelace
<https://shoelace.style>`__ or `Textual <https://textual.textualize.io>`__ API
documentation) to work out why a widget isn't behaving as expected.

If you're able to fix the problem, you'll need to add tests for :ref:`the core
API <run-core-test-suite>` and/or :ref:`the testbed backend <run-testbed>` for
that widget, depending on whether the fix was in the core API or to the backend
(or both).

Even if you can't fix the problem, reporting anything you discover as a comment
on the ticket is worthwhile. If you can find the source of the problem, but not
the fix, that knowledge will often be enough for someone who knows more about a
platform to solve the problem. Even a good reproduction case (a sample app that
does nothing but reproduce the problem) can be a huge help.

Contribute improvements to documentation
----------------------------------------

We've got a :doc:`separate contribution guide <./contribute-docs>` for
documentation contributions. This covers how to set up your development
environment to build Toga's documentation, and separate ideas for what to work
on.

Implement a platform native widget
----------------------------------

If the core library already specifies an interface for a widget, but the widget isn't
implemented on your platform of choice, implement that interface. The :doc:`supported
widgets by platform </reference/widgets_by_platform>` table can show you the widgets
that are missing on various platforms. You can also look for log messages in a running
app (or the direct ``factory.not_implemented()`` function calls that produce those log
messages). At present, the Web and Textual backends have the most missing widgets. If
you have web skills, or would like to learn more about `PyScript
<https://pyscript.net>`__ and `Shoelace <https://shoelace.style>`__, the web backend
could be a good place to contribute; if you'd like to learn more about terminal
applications and the or `Textual <https://textual.textualize.io>`__ API, contributing to
the Textual backend could be a good place for you to contribute.

Alternatively, if there's a widget that doesn't exist, propose an interface
design, and implement it for at least one platform. You may find `this
presentation by BeeWare emeritus team member Dan Yeaw
<https://www.youtube.com/watch?v=sWt_sEZUiY8>`__ helpful. This talk gives an
architectural overview of Toga, as well as providing a guide to the process of
adding new widgets.

If you implement a new widget, don't forget you'll need to write tests for the
new core API. If you're extending an existing widget, you may need to :ref:`add
a probe for the backend <testbed-probe>`.

Add a new feature to an existing widget
---------------------------------------

Can you think of a feature than an existing widget should have? Propose a new
API for that widget, and provide a sample implementation. If you don't have any
ideas of your own, the Toga issue tracker has some `existing feature suggestions
<https://github.com/beeware/toga/issues?q=is%3Aopen+is%3Aissue+label%3Aenhancement>`__
that you could try to implement.

Again, you'll need to add unit tests and/or backend probes for any new features
you add.

Implement an entirely new platform backend
------------------------------------------

Toga currently has support for 7 backends - but there's room for more! In
particular, we'd be interested in seeing a `Qt-based backend
<https://github.com/beeware/toga/issues/1142>`__ to support KDE-based Linux
desktops.

The first steps of any new platform backend are always the same:

1. Implement enough of the Toga Application and Window classes to allow you to
   create an empty application window, integrated with the Python ``asyncio``
   event loop.
2. Work out how to use native platform APIs to position a widget at a specific
   position on the window. Most widget frameworks will have some sort of native
   layout scheme; we need to replace that scheme with Toga's layout algorithm.
   If you can work out how to place a button with a fixed size at a specific
   position on the screen, that's usually sufficient.
3. Get Tutorial 0 working. This is the simple case of a single box that contains
   a single button. To get this tutorial working, you'll need to implement the
   factory class for your new backend so that Toga can instantiate widgets on
   your new backend, and connect the Toga style applicator methods on the base
   widget that sets the position of widgets on the screen.

Once you have those core features in place, you can start implementing widgets
and other Toga features (like fonts, images, and so on).

Improve the testing API for application writers
-----------------------------------------------

The dummy backend exists to validate that Toga's internal API works as expected.
However, we would like it to be a useful resource for *application* authors as
well. Testing GUI applications is a difficult task; a Dummy backend would
potentially allow an end user to write an application, and validate behavior by
testing the properties of the Dummy. Think of it as a GUI mock - but one that is
baked into Toga as a framework. See if you can write a GUI app of your own, and
write a test suite that uses the Dummy backend to validate the behavior of that
app.

.. _run-core-test-suite:

Running the core test suite
===========================

Toga uses `tox <https://tox.wiki/en/latest/>`__ to manage the testing process.
To run the core test suite:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ tox -e py

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ tox -e py

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>tox -e py

You should get some output indicating that tests have been run. You may see
``SKIPPED`` tests, but shouldn't ever get any ``FAIL`` or ``ERROR`` test
results. We run our full test suite before merging every patch. If that process
discovers any problems, we don't merge the patch. If you do find a test error or
failure, either there's something odd in your test environment, or you've found
an edge case that we haven't seen before - either way, let us know!

At the end of the test output there should be a report of the coverage data that
was gathered::

    Name    Stmts   Miss Branch BrPart   Cover   Missing
    ----------------------------------------------------
    TOTAL    4345      0   1040      0  100.0%

This tells us that the test suite has executed every possible branching path
in the ``toga-core`` library. This isn't a 100% guarantee that there are no bugs,
but it does mean that we're exercising every line of code in the core API.

If you make changes to the core API, it's possible you'll introduce a gap in this
coverage. When this happens, the coverage report will tell you which lines aren't
being executed. For example, lets say we made a change to ``toga/window.py``,
adding some new logic. The coverage report might look something like::

  Name                 Stmts   Miss Branch BrPart  Cover   Missing
  ----------------------------------------------------------------
  src/toga/window.py     186      2     22      2  98.1%   211, 238-240
  ----------------------------------------------------------------
  TOTAL                 4345      2   1040      2  99.9%

This tells us that line 211, and lines 238-240 are not being executed by the test
suite. You'll need to add new tests (or modify an existing test) to restore this
coverage.

When you're developing your new test, it may be helpful to run *just* that one
test. To do this, you can pass in the name of a specific test file (or a
specific test, using `pytest specifiers
<https://docs.pytest.org/en/latest/how-to/usage.html>`__):

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ tox -e py -- tests/path_to_test_file/test_some_test.py

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ tox -e py -- tests/path_to_test_file/test_some_test.py

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>tox -e py -- tests/path_to_test_file/test_some_test.py

These test paths are relative to the ``core`` directory. You'll still get a
coverage report when running a part of the test suite - but the coverage results
will only report the lines of code that were executed by the specific tests you
ran.

.. _run-testbed:

Running the testbed
===================

The core API tests exercise ``toga-core`` - but what about the backends? To verify
the behavior of the backends, Toga has a testbed app. This app uses the core API
to exercise all the behaviors that the backend APIs need to perform - but uses
an actual platform backend to implement that behavior.

To run the testbed app, install `Briefcase
<https://briefcase.readthedocs.io/en/latest/>`__, and run the app in developer
test mode:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ python -m pip install briefcase
      (venv) $ cd testbed
      (venv) $ briefcase dev --test

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ python -m pip install briefcase
      (venv) $ cd testbed
      (venv) $ briefcase dev --test

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>python -m pip install briefcase
      (venv) C:\...>cd testbed
      (venv) C:\...>briefcase dev --test

This will display a Toga app window, which will flash as it performs all the GUI
tests. You'll then see a coverage report for the code that has been executed.

If you want to run a subset of the entire test suite, Briefcase honors `pytest
specifiers <https://docs.pytest.org/en/latest/how-to/usage.html>`__) in the same
way as the main test suite.

The testbed app provides one additional feature that the core tests don't have --
slow mode. Slow mode runs the same tests, but deliberately pauses for 1 second
between each GUI action so that you can observe what is going on.

So - to run *only* the button tests in slow mode, you could run:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ briefcase dev --test -- tests/widgets/test_button.py --slow

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ briefcase dev --test -- tests/widgets/test_button.py --slow

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>briefcase dev --test -- tests/widgets/test_button.py --slow

This test will take a lot longer to run, but you'll see the widget (Button, in
this case) go through various color, format, and size changes as the test runs.
You won't get a coverage report if you run a subset of the tests, or if you
enable slow mode.

Developer mode is useful for testing desktop platforms (Cocoa, Winforms and
GTK); but if you want to test a mobile backend, you'll need to use ``briefcase
run``.

.. tabs::

  .. group-tab:: macOS

    To run the Android test suite:

    .. code-block:: console

      (venv) $ briefcase run android --test

    To run the iOS test suite:

    .. code-block:: console

      (venv) $ briefcase run iOS --test

  .. group-tab:: Linux

    To run the Android test suite:

    .. code-block:: console

      (venv) $ briefcase run android --test

    iOS tests can't be executed on Linux.

  .. group-tab:: Windows

    To run the Android test suite:

    .. code-block:: doscon

      (venv) C:\...>briefcase run android --test

    iOS tests can't be executed on Windows.

You can also use slow mode or pytest specifiers with ``briefcase run``, using
the same ``--`` syntax as you used in developer mode.

.. _testbed-probe:

How the testbed works
---------------------

The testbed works by providing a generic collection of behavioral tests on a
live app, and then providing an API to instrument the live app to verify that
those behaviors have been implemented. That API is then implemented by each
backend.

The implementation of the generic behavioral tests is contained in the `tests
folder of the testbed app
<https://github.com/beeware/toga/tree/main/testbed/tests>`__. These tests use
the public API of a widget to exercise all the corner cases of each
implementation. Some of the tests are generic (for example, setting the
background color of a widget) and are shared between widgets, but each widget
has its own set of specific tests. These tests are all declared ``async``
because they need to interact with the event loop of a running application.

Each test will make a series of calls on a widget's public API. The public API
is used to verify the behavior that an end user would experience when
programming a Toga app. The test will *also* make calls on the `probe` for the
widget.

The widget probe provides a generic interface for interacting with the internals
of widget, verifying that the implementation is in the correct state as a result
of invoking a public API. The probes for each platform are implemented in the
``tests_backend`` folder of each backend. For example, the Cocoa tests backend
and probe implementations can be found `here
<https://github.com/beeware/toga/tree/main/cocoa/tests_backend>`__.

The probe for each widget provides a way to manipulate and inspect the internals
of a widget in a way that may not be possible from a public API. For example,
the Toga public API doesn't provide a way to determine the physical size of a
widget, or interrogate the font being used to render a widget; the probe
implementation does. This allows a testbed test case to verify that a widget has
been laid out correctly inside the Toga window, is drawn using the right font,
and has any other other appropriate physical properties or internal state.

The probe also provides a programmatic interface for interacting *with* a
widget. For example, in order to test a button, you need to be able to press
that button; the probe API provides an API to simulate that press. This allows
the testbed to verify that the correct callbacks will be invoked when a button
is pressed. These interactions are performed by generating events in the GUI
framework being tested.

The widget probe also provides a ``redraw()`` method. GUI libraries don't always
immediately apply changes visually, as graphical changes will often be batched
so that they can be applied in a single redraw. To ensure that any visual
changes have been applied before a test asserts the properties of the app, a
test case can call ``await probe.redraw()``. This guarantees that any
outstanding redraw events have been processed. These ``redraw()`` requests are
also used to implement slow mode - each redraw is turned into a 1 second sleep.

If a widget doesn't have a probe for a given widget, the testbed should call
``pytest.skip()`` for that platform when constructing the widget fixture (there
is a ``skip_on_platforms()`` helper method in the testbed method to do this).
If a widget hasn't implemented a specific probe method that the testbed
required, it should call ``pytest.skip()`` so that the backend knows to skip the
test.

If a widget on a given backend doesn't support a given feature, it should use
``pytest.xfail()`` (expected failure) for the probe method testing that feature.
For example, Cocoa doesn't support setting the text color of buttons; as a
result, the Cocoa implementation of the ``color`` `property of the Button probe
<https://github.com/beeware/toga/blob/main/cocoa/tests_backend/widgets/button.py#L17>`__
performs an ``xfail`` describing that limitation.

.. _pr-housekeeping:

Submitting a pull request
=========================

Before you submit a pull request, there's a few bits of housekeeping to do.

Submit from a feature branch, not your ``main`` branch
------------------------------------------------------

Before you start working on your change, make sure you've created a branch.
By default, when you clone your repository fork, you'll be checked out on
your ``main`` branch. This is a direct copy of Toga's ``main`` branch.

While you *can* submit a pull request from your ``main`` branch, it's preferable
if you *don't* do this. If you submit a pull request that is *almost* right, the
core team member who reviews your pull request may be able to make the necessary
changes, rather than giving feedback asking for a minor change. However, if you
submit your pull request from your ``main`` branch, reviewers are prevented from
making modifications.

Instead, you should make your changes on a *feature branch*. A feature branch
has a simple name to identify the change that you've made. For example, if
you've found a bug in Toga's layout algorithm, you might create a feature branch
``fix-layout-bug``. If your bug relates to a specific issue that has been
reported, it's also common to reference that issue number in the branch name
(e.g., ``fix-1234``).

To create a feature branch, run:

.. tabs::

  .. group-tab:: macOS

    .. code-block:: console

      (venv) $ git checkout -b fix-layout-bug

  .. group-tab:: Linux

    .. code-block:: console

      (venv) $ git checkout -b fix-layout-bug

  .. group-tab:: Windows

    .. code-block:: doscon

      (venv) C:\...>git checkout -b fix-layout-bug

Commit your changes to this branch, then push to GitHub and create a pull request.

Add change information for release notes
----------------------------------------

Before you submit this change as a pull request, you need to add a *change note*.
Toga uses `towncrier <https://pypi.org/project/towncrier/>`__ to
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

See `News Fragments
<https://towncrier.readthedocs.io/en/stable/tutorial.html#creating-news-fragments>`__
for more details on the types of news fragments you can add. You can also see
existing examples of news fragments in the ``changes/`` folder. Name the file
using the number of the issue that your pull request is addressing. When there
isn't an existing issue, you can create the pull request in two passes: First
submit it without a change note - this will fail, but will also assign a pull
request number. You can then push an update to the pull request, adding the
change note with the assigned number.

It's not just about coverage!
-----------------------------

Although we're always trying to improve test coverage, the
task isn't *just* about increasing the numerical coverage value. Part of the
task is to audit the code as you go. You could write a comprehensive set of
tests for a concrete life jacket... but a concrete life jacket would still be
useless for the purpose it was intended!

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

Waiting for feedback
--------------------

Once you've written your code, test, and change note, you can submit your
changes as a pull request. One of the core team will review your work, and
give feedback. If any changes are requested, you can make those changes, and
update your pull request; eventually, the pull request will be accepted and
merged. Congratulations, you're a contributor to Toga!

What next?
==========

Rinse and repeat! If you've improved coverage by one line, go back and do it
again for *another* coverage line! If you've implemented a new widget, implement
*another* widget!

Most importantly - have fun!
