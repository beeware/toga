# Contributing to Toga's documentation

You might have the best software in the world - but if nobody knows how to use it, what's the point? Documentation can always be improved - and we need your help!

Toga's documentation is written using [MkDocs and Markdown](https://www.markdownguide.org/basic-syntax/). We aim to follow the [Diataxis](https://diataxis.fr) framework for structuring documentation.

## Building Toga's documentation

To build Toga's documentation, start by ensuring you [have the prerequisites][dev-environment-prereqs], and then [set up a development environment][dev-environment-tldr] (or, for a more detailed explanation of dev environment setup, [start here][setup-dev-environment]).You **must** have a Python 3.12 interpreter installed and available on your path (i.e., `python3.12` must start a Python 3.12 interpreter).

### Build documentation locally

Once your development environment is set up, run:

/// tab | macOS

```console
(venv) $ tox -e docs
```

///

/// tab | Linux

```console
(venv) $ tox -e docs
```

///

/// tab | Windows

```doscon
(venv) C:\...>tox -e docs
```

///

The output of the file should be in the `docs/_build/html` folder. If there are any markup problems, they'll raise an error.

### Live documentation preview

To support rapid editing of documentation, Toga also has a "live preview" mode:

/// tab | macOS

```console
(venv) $ tox -e docs-live
```

///

/// tab | Linux

```console
(venv) $ tox -e docs-live
```

///

/// tab | Windows

```doscon
(venv) C:\...>tox -e docs-live
```

///

This will build the documentation, start a web server to serve the build documentation, and watch the file system for any changes to the documentation source. If a change is detected, the documentation will be rebuilt, and any browser viewing the modified page will be automatically refreshed.

Live preview mode will also monitor any changes to the `core/src` folder, reflecting any changes to inline documentation.

### Documentation linting

The build process will identify many issues within the Markdown, but Toga performs some additional "lint" checks. To run the lint checks:

/// tab | macOS

```console
(venv) $ tox -e docs-lint
```

///

/// tab | Linux

```console
(venv) $ tox -e docs-lint
```

///

/// tab | Windows

```doscon
(venv) C:\...>tox -e docs-lint
```

///

This will validate the documentation does not contain:

- dead hyperlinks
- misspelled words

If a valid spelling of a word is identified as misspelled, then add the word to the list in `docs/spelling_wordlist`. This will add the word to the spellchecker's dictionary. When adding to this list, remember:

- We prefer US spelling, with some liberties for programming-specific colloquialism (e.g., "apps") and verbing of nouns (e.g., "scrollable")
- Any reference to a product name should use the product's preferred capitalization. (e.g., "macOS", "GTK", "pytest", "Pygame", "PyScript").
- If a term is being used "as code", then it should be quoted as a literal rather than being added to the dictionary.

## What to work on?

If you're looking for specific areas to improve, there are [tickets tagged "documentation"](https://github.com/beeware/toga/issues?q=is%3Aopen+is%3Aissue+label%3Adocumentation) in Toga's issue tracker.

However, you don't need to be constrained by these tickets. If you can identify a gap in Toga's documentation, or an improvement that can be made, start writing! Anything that improves the experience of the end user is a welcome change.

## Submitting a pull request

Before you submit a pull request, there's a few bits of housekeeping to do. See the section on submitting a pull request in the [code contribution guide][pr-housekeeping] for details on our submission process.
