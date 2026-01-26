{{ component_header("Source") }}

## Usage

Data sources are abstractions that allow you to define the data being managed by your application independent of the GUI representation of that data. For details on the use of data sources, see the [topic guide](/topics/data-sources.md).

The base class referenced on this page, [`Source`][toga.sources.Source], isn't useful on its own. It provides an implementation of the notification API that data sources must provide, and is subclassed by:

- [ListSource](listsource.md)
- [TreeSource](treesource.md)
- [ValueSource](valuesource.md)

It can also be used by custom data source implementations.

## Reference

::: toga.sources.Source
