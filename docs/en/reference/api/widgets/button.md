# Button

A button that can be pressed or clicked.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/button-cocoa.png" width="300"
alt="/reference/images/button-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/button-gtk.png" width="300"
alt="/reference/images/button-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/button-winforms.png" width="300"
alt="/reference/images/button-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/button-android.png" width="300"
alt="/reference/images/button-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/button-iOS.png" width="300"
alt="/reference/images/button-iOS.png" />
</figure>
:::

::: {.group-tab}
Web [\|beta\|](##SUBST##|beta|)

<figure class="align-center">
<img src="/reference/images/button-web.png" width="300"
alt="/reference/images/button-web.png" />
</figure>
:::

::: {.group-tab}
Textual [\|beta\|](##SUBST##|beta|)

Screenshot not available
:::
::::::::::

## Usage

A button has a text label, or an icon (but not both). If an icon is
specified, it will be resized to a size appropriate for the platform. A
handler can be associated with button press events.

``` python
import toga

def my_callback(button):
    # handle event
    pass

button = toga.Button("Click me", on_press=my_callback)

icon_button = toga.Button(icon=toga.Icon("resources/my_icon"), on_press=my_callback)
```

## Notes

- A background color of `TRANSPARENT` will be treated as a reset of the
  button to the default system color.
- On macOS, the button text color cannot be set directly; any `color`
  style directive will be ignored. The text color is automatically
  selected by the platform to contrast with the background color of the
  button.

## Reference

::: {.autoclass}
toga.Button
:::

::: {.autoprotocol}
toga.widgets.button.OnPressHandler
:::
