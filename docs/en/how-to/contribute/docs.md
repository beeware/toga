# Contributing to Toga's documentation

You might have the best software in the world - but if nobody knows how
to use it, what's the point? Documentation can always be improved - and
we need need your help!

Toga's documentation is written using [Sphinx and
reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html).
We aim to follow the [Diataxis](https://diataxis.fr) framework for
structuring documentation.

## Building Toga's documentation

To build Toga's documentation, start by ensuring you
`have the prerequisites
<dev-environment-prereqs>`{.interpreted-text role="ref"}, and then
`set up a development environment
<dev-environment-tldr>`{.interpreted-text role="ref"} (or, for a more
detailed explanation of dev environment setup,
`start here <setup-dev-environment>`{.interpreted-text role="ref"}).You
**must** have a Python 3.12 interpreter installed and available on your
path (i.e., `python3.12` must start a Python 3.12 interpreter).

You'll also need to install the Enchant spell checking library.

:::::: {.tabs}
::: {.group-tab}
macOS

Enchant can be installed using [Homebrew](https://brew.sh):

``` console
(venv) $ brew install enchant
```

If you're on an Apple Silicon machine (M-series), you'll also need to
manually set the location of the Enchant library:

``` console
(venv) $ export PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.2.dylib
```
:::

::: {.group-tab}
Linux

Enchant can be installed as a system package:

**Ubuntu / Debian**

``` console
$ sudo apt update
$ sudo apt install enchant-2
```

**Fedora**

``` console
$ sudo dnf install enchant
```

**Arch / Manjaro**

``` console
$ sudo pacman -Syu enchant
```

**OpenSUSE Tumbleweed**

``` console
$ sudo zypper install enchant
```
:::

::: {.group-tab}
Windows

Enchant is installed automatically when you set up your development
environment.
:::
::::::

### Build documentation locally

Once your development environment is set up, run:

:::::: {.tabs}
::: {.group-tab}
macOS

``` console
(venv) $ tox -e docs
```
:::

::: {.group-tab}
Linux

``` console
(venv) $ tox -e docs
```
:::

::: {.group-tab}
Windows

``` doscon
(venv) C:\...>tox -e docs
```
:::
::::::

The output of the file should be in the `docs/_build/html` folder. If
there are any markup problems, they'll raise an error.

### Live documentation preview

To support rapid editing of documentation, Toga also has a "live
preview" mode:

:::::: {.tabs}
::: {.group-tab}
macOS

``` console
(venv) $ tox -e docs-live
```
:::

::: {.group-tab}
Linux

``` console
(venv) $ tox -e docs-live
```
:::

::: {.group-tab}
Windows

``` doscon
(venv) C:\...>tox -e docs-live
```
:::
::::::

This will build the documentation, start a web server to serve the build
documentation, and watch the file system for any changes to the
documentation source. If a change is detected, the documentation will be
rebuilt, and any browser viewing the modified page will be automatically
refreshed.

Live preview mode will only monitor the `docs` directory for changes. If
you're updating the inline documentation associated with Toga source
code, you'll need to use the `docs-live-src` target to build docs:

:::::: {.tabs}
::: {.group-tab}
macOS

``` console
(venv) $ tox -e docs-live-src
```
:::

::: {.group-tab}
Linux

``` console
(venv) $ tox -e docs-live-src
```
:::

::: {.group-tab}
Windows

``` doscon
(venv) C:\...>tox -e docs-live-src
```
:::
::::::

This behaves the same as `docs-live`, but will also monitor any changes
to the `core/src` folder, reflecting any changes to inline
documentation. However, the rebuild process takes much longer, so you
may not want to use this target unless you're actively editing inline
documentation.

### Documentation linting

The build process will identify reStructuredText problems, but Toga
performs some additional "lint" checks. To run the lint checks:

:::::: {.tabs}
::: {.group-tab}
macOS

``` console
(venv) $ tox -e docs-lint
```
:::

::: {.group-tab}
Linux

``` console
(venv) $ tox -e docs-lint
```
:::

::: {.group-tab}
Windows

``` doscon
(venv) C:\...>tox -e docs-lint
```
:::
::::::

This will validate the documentation does not contain:

- invalid syntax and markup
- dead hyperlinks
- misspelled words

If a valid spelling of a word is identified as misspelled, then add the
word to the list in `docs/spelling_wordlist`. This will add the word to
the spellchecker's dictionary. When adding to this list, remember:

- We prefer US spelling, with some liberties for programming-specific
  colloquialism (e.g., "apps") and verbing of nouns (e.g., "scrollable")
- Any reference to a product name should use the product's preferred
  capitalization. (e.g., "macOS", "GTK", "pytest", "Pygame",
  "PyScript").
- If a term is being used "as code", then it should be quoted as a
  literal rather than being added to the dictionary.

### Rebuilding all documentation

To force a rebuild for all of the documentation:

:::::: {.tabs}
::: {.group-tab}
macOS

``` console
(venv) $ tox -e docs-all
```
:::

::: {.group-tab}
Linux

``` console
(venv) $ tox -e docs-all
```
:::

::: {.group-tab}
Windows

``` doscon
(venv) C:\...>tox -e docs-all
```
:::
::::::

The documentation should be fully rebuilt in the `docs/_build/html`
folder. If there are any markup problems, they'll raise an error.

## What to work on?

If you're looking for specific areas to improve, there are [tickets
tagged
"documentation"](https://github.com/beeware/toga/issues?q=is%3Aopen+is%3Aissue+label%3Adocumentation)
in Toga's issue tracker.

However, you don't need to be constrained by these tickets. If you can
identify a gap in Toga's documentation, or an improvement that can be
made, start writing! Anything that improves the experience of the end
user is a welcome change.

## Submitting a pull request

Before you submit a pull request, there's a few bits of housekeeping to
do. See the section on submitting a pull request in the
`code contribution guide
<pr-housekeeping>`{.interpreted-text role="ref"} for details on our
submission process.
