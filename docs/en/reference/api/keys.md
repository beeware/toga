# Keys

A symbolic representation of keys used for keyboard shortcuts.

Most keys have a constant that matches the text on the key, or the name
of the key if the text on the key isn't a legal Python identifier.

However, due to differences between platforms, there's no representation
of "modifier" keys like Control, Command, Option, or the Windows Key.
Instead, Toga provides three generic modifier constants, and maps those
to the modifier keys, matching the precedence with which they are used
on the underlying platforms:

<table>
<thead>
<tr>
<th>Platform</th>
<th><code class="interpreted-text" role="any">MOD_1</code></th>
<th><code class="interpreted-text" role="any">MOD_2</code></th>
<th><code class="interpreted-text" role="any">MOD_3</code></th>
</tr>
</thead>
<tbody>
<tr>
<td><blockquote>
<p>Linux</p>
</blockquote></td>
<td><blockquote>
<p>Control</p>
</blockquote></td>
<td><blockquote>
<p>Alt</p>
</blockquote></td>
<td><blockquote>
<p>Tux/Windows/Meta</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p>macOS</p>
</blockquote></td>
<td><blockquote>
<p>Command (⌘)</p>
</blockquote></td>
<td><blockquote>
<p>Option</p>
</blockquote></td>
<td><blockquote>
<p>Control (^)</p>
</blockquote></td>
</tr>
<tr>
<td><blockquote>
<p>Windows</p>
</blockquote></td>
<td><blockquote>
<p>Control</p>
</blockquote></td>
<td><blockquote>
<p>Alt</p>
</blockquote></td>
<td><blockquote>
<p>Not supported</p>
</blockquote></td>
</tr>
</tbody>
</table>

Key combinations can be expressed by combining multiple `Key` values
with the `+` operator.

``` python
from toga import Key

just_an_a = Key.A
shift_a = Key.SHIFT + Key.A
# Windows/Linux - Control-Shift-A:
# macOS - Command-Shift-A:
modified_shift_a = Key.MOD_1 + Key.SHIFT + Key.A
```

The order of addition is not significant. `Key.SHIFT + Key.A` and
`Key.A + Key.SHIFT` will produce the same key representation.

## Reference

::: {.autoclass}
toga.Key
:::
