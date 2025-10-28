{{ component_header("DocumentWindow", width=450, alt_file="mainwindow") }}

## Usage

A DocumentWindow is the same as a [`toga.MainWindow`][], except that it is bound to a [`toga.Document`][] instance, exposed as the [`toga.DocumentWindow.doc`][] attribute.

Instances of [`toga.DocumentWindow`][] should be created as part of the [`create()`][toga.Document.create] method of an implementation of [`toga.Document`][].

## Reference

::: toga.DocumentWindow
