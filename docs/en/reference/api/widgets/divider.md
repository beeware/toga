# Divider

A separator used to visually distinguish two sections of content in a
layout.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/divider-cocoa.png" width="300"
alt="/reference/images/divider-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/divider-gtk.png" width="300"
alt="/reference/images/divider-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/divider-winforms.png" width="300"
alt="/reference/images/divider-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/divider-android.png" width="300"
alt="/reference/images/divider-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/divider-iOS.png" width="300"
alt="/reference/images/divider-iOS.png" />
</figure>
:::

::: {.group-tab}
Web [\|beta\|](##SUBST##|beta|)

Screenshot not available
:::

::: {.group-tab}
Textual [\|no\|](##SUBST##|no|)

Not supported
:::
::::::::::

## Usage

To separate two labels stacked vertically with a horizontal line:

``` python
import toga
from toga.style.pack import Pack, COLUMN

box = toga.Box(
    children=[
        toga.Label("First section"),
        toga.Divider(),
        toga.Label("Second section"),
    ],
    direction=COLUMN,
    flex=1,
    margin=10
)
```

The direction (horizontal or vertical) can be given as an argument. If
not specified, it will default to horizontal.

## Reference

::: {.autoclass}
toga.Divider
:::
