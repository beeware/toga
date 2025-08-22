# PasswordInput

A widget to allow the entry of a password. Any value typed by the user
will be obscured, allowing the user to see the number of characters they
have typed, but not the actual characters.

:::::::::: {.tabs}
::: {.group-tab}
macOS

<figure class="align-center">
<img src="/reference/images/passwordinput-cocoa.png" width="300"
alt="/reference/images/passwordinput-cocoa.png" />
</figure>
:::

::: {.group-tab}
Linux

<figure class="align-center">
<img src="/reference/images/passwordinput-gtk.png" width="300"
alt="/reference/images/passwordinput-gtk.png" />
</figure>
:::

::: {.group-tab}
Windows

<figure class="align-center">
<img src="/reference/images/passwordinput-winforms.png" width="300"
alt="/reference/images/passwordinput-winforms.png" />
</figure>
:::

::: {.group-tab}
Android

<figure class="align-center">
<img src="/reference/images/passwordinput-android.png" width="300"
alt="/reference/images/passwordinput-android.png" />
</figure>
:::

::: {.group-tab}
iOS

<figure class="align-center">
<img src="/reference/images/passwordinput-iOS.png" width="300"
alt="/reference/images/passwordinput-iOS.png" />
</figure>
:::

::: {.group-tab}
Web

<figure class="align-center">
<img src="/reference/images/passwordinput-web.png" width="300"
alt="/reference/images/passwordinput-web.png" />
</figure>
:::

::: {.group-tab}
Textual [\|no\|](##SUBST##|no|)

Not supported
:::
::::::::::

## Usage

The `PasswordInput` is functionally identical to a
`~toga.TextInput`{.interpreted-text role="class"}, except for how the
text is displayed. All features supported by
`~toga.TextInput`{.interpreted-text role="class"} are also supported by
PasswordInput.

``` python
import toga

password = toga.PasswordInput()
```

## Notes

- Winforms does not support the use of partially or fully transparent
  colors for the PasswordInput background. If a color with an alpha
  value is provided (including `TRANSPARENT`), the alpha channel will be
  ignored. A `TRANSPARENT` background will be rendered as white.
- On Winforms, if a PasswordInput is given an explicit height, the
  rendered widget will not expand to fill that space. The widget will
  have the fixed height determined by the font used on the widget. In
  general, you should avoid setting a `height` style property on
  PasswordInput widgets.

## Reference

::: {.autoclass}
toga.PasswordInput
:::
