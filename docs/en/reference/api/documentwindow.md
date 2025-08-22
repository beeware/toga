# DocumentWindow

A window that can be used as the main interface to a document-based app.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/mainwindow-cocoa.png" width="450"
alt="/reference/images/mainwindow-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/mainwindow-gtk.png" width="450"
alt="/reference/images/mainwindow-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/mainwindow-winforms.png" width="450"
alt="/reference/images/mainwindow-winforms.png" />
</figure>
:::

::: {.group-tab}
Android [\|no\|](##SUBST##|no|)

Not supported
:::

::: {.group-tab}
iOS [\|no\|](##SUBST##|no|)

Not supported
:::

::: {.group-tab}
Web [\|no\|](##SUBST##|no|)

Not supported
:::

::: {.group-tab}
Textual [\|no\|](##SUBST##|no|)

Not supported
:::
::::::::::

## Usage

A DocumentWindow is the same as a `toga.MainWindow`{.interpreted-text
role="any"}, except that it is bound to a
`toga.Document`{.interpreted-text role="any"} instance, exposed as the
`toga.DocumentWindow.doc`{.interpreted-text role="any"} attribute.

Instances of `toga.DocumentWindow`{.interpreted-text role="any"} should
be created as part of the `~toga.Document.create()`{.interpreted-text
role="meth"} method of an implementation of
`toga.Document`{.interpreted-text role="any"}.

## Reference

::: {.autoclass}
toga.DocumentWindow
:::
