# Examples

This directory contains example code demonstrating each widget defined by [Toga](https://toga.beeware.org).

It also contains working copies of the tutorial code.

## Running the examples

Each of the examples can run by copying the example code to your computer (either by cloning this repository, or by manually duplicating the specific files), installing Toga, and running the application as a Python module:

```console
$ cd <example name>
$ python -m <example name>
```

substituting the name of the example you want to run for `<example name>`.

## Backend compatibility

Not all examples are compatible with all Toga backends. This is due to the missing features in some backends.

| _Example_ (Folder) | macOS | Linux (GTK) | Linux (Qt) | Windows | iOS | Android | Web | Terminal |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `activityindicator` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `beeliza` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `box` | ✔️ | ❌ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `button` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `canvas` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `colors` | ✔️ | ✔️ | ❓ | ❓ | ❌ | ✔️ | ❌ | ❓ |
| `command` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `customwidget` | ✔️ | ✔️ | ✔️ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `date_and_time` | ✔️ | ❌ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `detailedlist` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `dialogs` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `divider` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `document` | ✔️ | ✔️ | ❓ | ❓ | ❌ | ❌ | ❌ | ❓ |
| `examples_overview` | ✔️ | ✔️ | ❓ | ❓ | ❌ | ❌ | ❌ | ❓ |
| `focus` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `font` | ✔️ | ✔️ | ❓ | ❓ | ❓ | ✔️ | ❌ | ❓ |
| `font_size` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `handlers` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `hardware` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `imageview` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `layout` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `mapview` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `multilinetextinput` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `numberinput` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `optioncontainer` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `passwordinput` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `positron-django` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ❓ | ❌ | ❓ |
| `positron-static` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `progressbar` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `resize` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `screenshot` | ✔️ | ✔️ | ✔️ | ❓ | ✔️ | ❓ | ❌ | ❓ |
| `scrollcontainer` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `selection` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `simpleapp` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `slider` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `splitcontainer` | ✔️ | ✔️ | ❓ | ❓ | ❌ | ❌ | ❌ | ❓ |
| `statusiconapp` | ✔️ | ❓ | ❓ | ❓ | ❌ | ❌ | ❌ | ❓ |
| `switches` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `table` | ✔️ | ✔️ | ❓ | ❓ | ❌ | ✔️ | ❌ | ❓ |
| `table_columns` | ✔️ | ✔️ | ❓ | ❓ | ❌ | ✔️ | ❌ | ❓ |
| `table_source` | ✔️ | ✔️ | ❓ | ❓ | ❌ | ✔️ | ❌ | ❓ |
| `textinput` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `tree` | ✔️ | ✔️ | ❓ | ❓ | ❌ | ❌ | ❌ | ❓ |
| `tree_source` | ✔️ | ❓ | ❓ | ❓ | ❌ | ❌ | ❌ | ❓ |
| `tutorial0` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `tutorial1` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ✔️ | ❓ |
| `tutorial2` | ✔️ | ✔️ | ❓ | ❓ | ❌ | ❌ | ❌ | ❓ |
| `tutorial3` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `tutorial4` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `webview` | ✔️ | ✔️ | ❓ | ❓ | ✔️ | ✔️ | ❌ | ❓ |
| `window` | ✔️ | ✔️ | ❓ | ❓ | ❌ | ❌ | ❌ | ❓ |
