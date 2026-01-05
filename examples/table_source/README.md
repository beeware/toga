# Table Source

An example of using a custom data source with a
[Table widget](https://toga.beeware.org/en/stable/reference/api/widgets/table.html).

This is the same example as Table; but instead of using lists, the code
provides a custom data source that wraps the concept of movies. This is
a more realistic example of what you'd do in practice with a table.

It also uses the data source as the items of a Selection widget. When
the data source changes, the options available in the Selection widget
will match the changes.

## Quickstart

To run this example:

```
$ python -m pip install toga
$ python -m table_source
```
