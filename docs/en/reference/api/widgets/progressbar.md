{{ component_header("ProgressBar", width=300) }}

## Usage

The task being monitored can be of known or indeterminate length.

If a progress bar has a `max` value, it is a *determinate* progress bar. The value of the progress bar can be altered over time, indicating progress on a task. The visual indicator of the progress bar will be filled indicating the proportion of `value` relative to `max`. `max` can be any positive numerical value.

```python
import toga

progress = toga.ProgressBar(max=100, value=1)

# Start progress animation
progress.start()

# Update progress to 10%
progress.value = 10

# Stop progress animation
progress.stop()
```

If a progress bar does *not* have a `max` value (i.e., `max == None`), it is an *indeterminate* progress bar. Any change to the value of an indeterminate progress bar will be ignored. When started, an indeterminate progress bar animates as a throbbing or "ping pong" animation.

```python
import toga

progress = toga.ProgressBar(max=None)

# Start progress animation
progress.start()

# Stop progress animation
progress.stop()
```

## Notes

- The visual appearance of progress bars varies from platform to platform. Toga will try to provide a visual distinction between running and not-running determinate progress bars, but this cannot be guaranteed.

## Reference

::: toga.ProgressBar
