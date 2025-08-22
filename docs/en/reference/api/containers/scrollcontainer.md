# ScrollContainer

A container that can display a layout larger than the area of the
container, with overflow controlled by scroll bars.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/scrollcontainer-cocoa.png" width="450"
alt="/reference/images/scrollcontainer-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/scrollcontainer-gtk.png" width="450"
alt="/reference/images/scrollcontainer-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/scrollcontainer-winforms.png" width="450"
alt="/reference/images/scrollcontainer-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/scrollcontainer-android.png" width="450"
alt="/reference/images/scrollcontainer-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/scrollcontainer-iOS.png" width="450"
alt="/reference/images/scrollcontainer-iOS.png" />
</figure>
:::

::: {.group-tab}
Web

<figure class="align-center">
<img src="/reference/images/scrollcontainer-web.png" width="450"
alt="/reference/images/scrollcontainer-web.png" />
</figure>
:::

::: {.group-tab}
Textual [\|no\|](##SUBST##|no|)

Not supported
:::
::::::::::

## Usage

``` python
import toga

content = toga.Box(children=[...])

container = toga.ScrollContainer(content=content)
```

## Reference

::: {.autoclass exclude-members="window, app"}
toga.ScrollContainer
:::

::: {.autoprotocol}
toga.widgets.scrollcontainer.OnScrollHandler
:::
