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

### Updating progress without blocking the interface

Toga updates the interface on the same event loop that runs asynchronous [event handlers](../../../topics/api-design.md#events). A synchronous handler that performs a long loop, calls `time.sleep()`, or waits for blocking I/O prevents the interface from redrawing, so progress changes will not become visible until the handler returns.

Use an `async` handler and `await` operations that yield control to the event loop. This complete app simulates an asynchronous task and updates the progress bar after each step:

```python
import asyncio

import toga


class ProgressApp(toga.App):
    def startup(self):
        self.progress = toga.ProgressBar(max=100)
        self.run_button = toga.Button("Run task", on_press=self.run_task)

        self.main_window = toga.MainWindow()
        self.main_window.content = toga.Box(
            children=[self.progress, self.run_button],
            direction="column",
            gap=10,
            margin=10,
        )
        self.main_window.show()

    async def run_task(self, button, **kwargs):
        button.enabled = False
        self.progress.value = 0
        self.progress.start()

        try:
            for step in range(1, 101):
                await asyncio.sleep(0.05)
                self.progress.value = step
        finally:
            self.progress.stop()
            button.enabled = True


def main():
    return ProgressApp("Progress", "org.example.progress")
```

The `on_press` handler does not need to return a value; the task is complete when the coroutine returns. Replace `asyncio.sleep()` with calls to an asynchronous I/O library in a real application.

If the work uses a blocking synchronous API, run each unit of work with [`asyncio.to_thread()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread), then update the progress bar after the `await`. Do not access Toga widgets from the worker thread.

The repository's [ProgressBar example](https://github.com/beeware/toga/tree/main/examples/progressbar) demonstrates additional determinate, indeterminate, manual, and automatic progress controls.

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
