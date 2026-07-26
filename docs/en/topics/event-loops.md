# Event loops

Toga applications update their interface on the same event loop that runs asynchronous
[event handlers](api-design.md#events). Code running in an event handler must return
control to that loop regularly so the interface can redraw and respond to user input.

## Keep the interface responsive

A synchronous handler that performs a long loop, calls `time.sleep()`, or waits for
blocking I/O prevents the interface from redrawing until the handler returns. Use an
`async` handler and `await` operations that yield control to the event loop instead.

This complete app simulates an asynchronous task and updates a
[`ProgressBar`][toga.ProgressBar] after each step:

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

The `on_press` handler does not need to return a value; the task is complete when the
coroutine returns. Replace `asyncio.sleep()` with calls to an asynchronous I/O library
in a real application.

## Working with blocking APIs

When work uses a blocking synchronous API, run each unit of work with
[`asyncio.to_thread()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.to_thread).
After the `await`, update Toga widgets from the event-loop thread. Do not access Toga
widgets from the worker thread.
