from collections import deque


class ReentrantQueueRunner:
    """A task runner that supports near-simultaneous calling.

    To ensure that only one task is run for near-simultaneous calls, a stack of tasks is
    used and only the first task in that stack is called. To run a new task the runner
    needs to be reset after each completed task.
    """

    def __init__(self):
        self._run_stack = []

    def __call__(self, task) -> bool:
        if task is None:
            return False

        self._run_stack.append(task)
        if self._run_stack[0] == task:
            task()

            return True
        return False

    def reset(self):
        self._run_stack = []


class ReentrantQueue(deque):
    """A synchronous queue that supports reentrant calls to append tasks.

    The queue is started whenever an entry is appended to the empty queue. Reentrant
    calls are supported by using a task runner that only allows one task at a time. The
    queue attempts to run tasks when a task is complete and when a task is appended to
    the queue.

    The need for this type of queue arises in cases where the Python code is being
    called asynchronously by an external process.
    """

    def __init__(self):
        self._runner = ReentrantQueueRunner()

    def __getitem__(self, index):
        try:
            return super().__getitem__(index)
        except IndexError:
            return None

    def append(self, task):
        super().append(task)
        self._run_next()

    def _wrap_task(self, task):
        """Wraps the tasks so that each task has a unique id."""
        if task is None:
            return

        def wrapped(task=task):
            return task()

        return wrapped

    def _run_next(self):
        if self._runner(self._wrap_task(self[0])):
            self.popleft()
            self._runner.reset()
            self._run_next()
