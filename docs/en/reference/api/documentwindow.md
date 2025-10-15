# DocumentWindow

A window that can be used as the main interface to a document-based app.

/// tab | macOS

![/reference/images/mainwindow-cocoa.png](/reference/images/mainwindow-cocoa.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | GTK

![/reference/images/mainwindow-gtk.png](/reference/images/mainwindow-gtk.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Qt {{ beta_support }}

![/reference/images/mainwindow-qt.png](/reference/images/mainwindow-qt.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Windows

![/reference/images/mainwindow-winforms.png](/reference/images/mainwindow-winforms.png){ width="450" }

/// caption

///

<!-- TODO: Update alt text -->

///

/// tab | Android {{ not_supported }}

Not supported

///

/// tab | iOS {{ not_supported }}

Not supported

///

/// tab | Web {{ not_supported }}

Not supported

///

/// tab | Textual {{ not_supported }}

Not supported

///

## Usage

A DocumentWindow is the same as a [`toga.MainWindow`][], except that it is bound to a [`toga.Document`][] instance, exposed as the [`toga.DocumentWindow.doc`][] attribute.

Instances of [`toga.DocumentWindow`][] should be created as part of the [`create()`][toga.Document.create] method of an implementation of [`toga.Document`][].

## Reference

::: toga.DocumentWindow
