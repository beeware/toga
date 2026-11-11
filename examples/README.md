# Examples

This directory contains example code demonstrating each widget defined by [Toga](https://toga.beeware.org).

It also contains working copies of the tutorial code (5 variants numbered 0-4).

There are also a couple of tools used for:

- the documentation, a `screenshot` generator (with a Qt variant)
- demonstrating _Positron_, in its `positron-django` and `positron-static` variants
- running the examples collectively, via `examples_overview`.

All other examples are focused on an individual widget.

## Running the examples

Most of the examples can run by copying the example code to your computer (either by cloning this repository, or by manually duplicating the specific files), installing Toga, and running the application as a Python module:

```console
$ cd <example name>
$ python -m <example name>
```

substituting the name of the example you want to run for `<example name>`.

## Backend compatibility

Not all examples are compatible with all Toga backends. This is due to the missing features in some backends.

To run with the default backend of your environment run as described above. To run with an alternative backend such as _Qt_ or _Textual_, ensure the appropriate `toga` package and its dependencies (such as `PySide6`) are installed and use the `TOGA_BACKEND` environment variable if needed.

While _Briefcase_ configurations **are** provided, with limited exception these are not intended as _Briefcase_ examples (see the _Briefcase_ documentation instead), they exist only to allow the testing on other platforms (iOS, Android, Web). You can then use `briefcase run ios` or `android` or `web`.

Some examples _do_ use Briefcase so please review the individual `README.md` that is included.
