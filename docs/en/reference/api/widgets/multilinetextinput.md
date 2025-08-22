# MultilineTextInput

A scrollable panel that allows for the display and editing of multiple
lines of text.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/multilinetextinput-cocoa.png" width="300"
alt="/reference/images/multilinetextinput-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/multilinetextinput-gtk.png" width="300"
alt="/reference/images/multilinetextinput-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/multilinetextinput-winforms.png" width="300"
alt="/reference/images/multilinetextinput-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/multilinetextinput-android.png" width="300"
alt="/reference/images/multilinetextinput-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/multilinetextinput-iOS.png" width="300"
alt="/reference/images/multilinetextinput-iOS.png" />
</figure>
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

``` python
import toga

textbox = toga.MultilineTextInput()
textbox.value = "Some text.\nIt can be multiple lines of text."
```

The input can be provided a placeholder value - this is a value that
will be displayed to the user as a prompt for appropriate content for
the widget. This placeholder will only be displayed if the widget has no
content; as soon as a value is provided (either by the user, or
programmatically), the placeholder content will be hidden.

## Notes

- Winforms does not support the use of partially or fully transparent
  colors for the MultilineTextInput background. If a color with an alpha
  value is provided (including `TRANSPARENT`), the alpha channel will be
  ignored. A `TRANSPARENT` background will be rendered as white.

## Reference

::: {.autoclass}
toga.MultilineTextInput
:::

::: {.autoprotocol}
toga.widgets.multilinetextinput.OnChangeHandler
:::
