# Label

A text label for annotating forms or interfaces.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/label-cocoa.png" width="300"
alt="/reference/images/label-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/label-gtk.png" width="300"
alt="/reference/images/label-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/label-winforms.png" width="300"
alt="/reference/images/label-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/label-android.png" width="300"
alt="/reference/images/label-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/label-iOS.png" width="300"
alt="/reference/images/label-iOS.png" />
</figure>
:::

::: {.group-tab}
Web [\|beta\|](##SUBST##|beta|)

<figure class="align-center">
<img src="/reference/images/label-web.png" width="300"
alt="/reference/images/label-web.png" />
</figure>
:::

::: {.group-tab}
Textual [\|beta\|](##SUBST##|beta|)

Screenshot not available
:::
::::::::::

## Usage

``` python
import toga

label = toga.Label("Hello world")
```

## Notes

- Winforms does not support a text alignment value of `JUSTIFIED`. If
  this alignment value is used, the label will default to left
  alignment.

## Reference

::: {.autoclass}
toga.Label
:::
