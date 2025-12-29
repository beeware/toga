# Writing, running, and testing code

{% extends "contribute/how/write-code.md" %}

{% block front_matter %}

To begin working on code, ensure you have a [development environment](dev-environment.md) set up, and you are [working on a branch](branches.md)

{% endblock %}

{% block end_matter %}

Once you have everything working, you can [submit a pull request](submit-pr.md) with your changes.

{% endblock %}

{% block testing_tox_command %}

- test suite for available Python versions for the core and Travertino
- code coverage reporting for the core and Travertino

{% endblock %}

{% block testing_running_additional %}

#### Testing Core  { #run-core-test-suite }

To run the core test suite:

/// tab | macOS

```console
(.venv) $ tox -m test-core
```

///

/// tab | Linux

```console
(.venv) $ tox -m test-core
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox -m test-core
```

///

As with the full test suite, this should report [100% test coverage][code-coverage]

#### Testing Travertino  { #run-travertino-test-suite }

In addition to the core library, the Toga repository also includes Travertino, a package that defines the lower-level layout mechanisms and style definitions which core then builds on. Its test suite can be run just like that of core:

/// tab | macOS

```console
(.venv) $ tox -m test-trav
```

///

/// tab | Linux

```console
(.venv) $ tox -m test-trav
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox -m test-trav
```

///

As with the full test suite, and the core, this should report [100% test coverage][code-coverage].

#### Testing Core and Travertino

You can run both the core and Travertino tests with one command:

/// tab | macOS

```console
(.venv) $ tox -m test
```

///

/// tab | Linux

```console
(.venv) $ tox -m test
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox -m test
```

///

This will run both test suites, and report the two coverage results one after the other. As with the previous tests, this should report [100% test coverage][code-coverage].


{% endblock %}

{% block testing_subset_additional %}

To run a Travertino test instead, add `-trav`:

/// tab | macOS

```console
(.venv) $ tox -e py-trav -- tests/path_to_test_file/test_some_test.py
```

///

/// tab | Linux

```console
(.venv) $ tox -e py-trav -- tests/path_to_test_file/test_some_test.py
```

///

/// tab | Windows

```doscon
(.venv) C:\...>tox -e py-trav -- tests/path_to_test_file/test_some_test.py
```

///

{% endblock %}

{% block testing_additional %}

### The testbed  { #run-testbed }

The above test suites exercise `toga-core` and `travertino` - but what about the backends? To verify the behavior of the backends, Toga has a testbed app. This app uses the core API to exercise all the behaviors that the backend APIs need to perform - but uses an actual platform backend to implement that behavior.

Details on how the testbed works can be found in the [Testbed topic guide][testbed-probe].

#### Running the testbed app

To run the testbed app, install [Briefcase](https://briefcase.readthedocs.io/en/latest/), and run the app in developer test mode as described below. Note that you should have only 1 backend -- the backend that you're planning to test -- installed in your virtual environment when running the test suite in developer mode.

/// tab | macOS

```console
(.venv) $ python -m pip install briefcase
(.venv) $ cd testbed
(.venv) $ briefcase dev --app testbed --test
```

///

/// tab | Linux

For testing the GTK3 backend:

```console
(.venv) $ python -m pip install briefcase
(.venv) $ cd testbed
(.venv) $ TOGA_BACKEND=toga_gtk briefcase dev --app testbed --test
```

For testing the GTK4 backend without libadwaita:

```console
(.venv) $ python -m pip install briefcase
(.venv) $ cd testbed
(.venv) $ TOGA_BACKEND=toga_gtk TOGA_GTK=4 TOGA_GTKLIB=None briefcase dev --app testbed --test
```

For testing the GTK4 backend with libadwaita:

```console
(.venv) $ python -m pip install briefcase
(.venv) $ cd testbed
(.venv) $ TOGA_BACKEND=toga_gtk TOGA_GTK=4 TOGA_GTKLIB=Adw briefcase dev --app testbed --test
```

For testing the Qt backend:

```console
(.venv) $ python -m pip install briefcase
(.venv) $ cd testbed
(.venv) $ TOGA_BACKEND=toga_qt briefcase dev --app testbed-qt --test
```

The GTK4 and Qt backends are experimental and only partially implemented, so a lot of tests will be skipped; filling in the gaps for the missing widgets would be an extremely helpful contribution.

///

/// tab | Windows

```doscon
(.venv) C:\...>python -m pip install briefcase
(.venv) C:\...>cd testbed
(.venv) C:\...>briefcase dev --app testbed --test
```

///

This will display a Toga app window, which will flash as it performs all the GUI tests. You'll then see a coverage report for the code that has been executed.

/// admonition | Step away from the keyboard!

While the testbed is running, you can't touch the keyboard or mouse - *at all*. The testbed works by triggering mouse clicks, and it is checking for behaviors like changes in widget and window focus. As a result, it is important that the testbed retains control of the app during testing.

///

#### Running a subset of the testbed suite and slow mode

If you want to run a subset of the entire test suite, Briefcase honors [`pytest` specifiers](https://docs.pytest.org/en/latest/how-to/usage.html) in the same way as the main test suite.

The testbed app provides one additional feature that the core tests don't have --slow mode. Slow mode runs the same tests, but deliberately pauses for 1 second between each GUI action so that you can observe what is going on.

So - to run *only* the button tests in slow mode, you could run:

/// tab | macOS

```console
(.venv) $ briefcase dev --app testbed --test -- tests/widgets/test_button.py --slow
```

///

/// tab | Linux

```console
(.venv) $ briefcase dev --app testbed --test -- tests/widgets/test_button.py --slow
```

or

```console
(.venv) $ briefcase dev --app testbed-qt --test -- tests/widgets/test_button.py --slow
```

///

/// tab | Windows

```doscon
(.venv) C:\...>briefcase dev --app testbed --test -- tests/widgets/test_button.py --slow
```

///

This test will take a lot longer to run, but you'll see the widget (Button, in this case) go through various color, format, and size changes as the test runs. You won't get a coverage report if you run a subset of the tests, or if you enable slow mode.

#### Running the testbed for mobile platforms

Developer mode is useful for testing desktop platforms (Cocoa, Winforms and GTK); but if you want to test a mobile backend, you'll need to use `briefcase run`.

/// tab | macOS

To run the Android test suite:

```console
(.venv) $ briefcase run android --app testbed --test
```

To run the iOS test suite:

```console
(.venv) $ briefcase run iOS --app testbed --test
```

///

/// tab | Linux

To run the Android test suite:

```console
(.venv) $ briefcase run android --app testbed --test
```

iOS tests can't be executed on Linux.

///

/// tab | Windows

To run the Android test suite:

```doscon
(.venv) C:\...>briefcase run android --app testbed --test
```

iOS tests can't be executed on Windows.

///

You can also use slow mode or `pytest` specifiers with `briefcase run`, using the same `--` syntax as you used in developer mode.

{% endblock %}
