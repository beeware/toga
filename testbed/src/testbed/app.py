import toga


class Testbed(toga.App):
    def startup(self):
        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = toga.Box(
            children=[
                toga.Label("Did you forget to use --test?"),
            ]
        )
        self.main_window.show()

        # FIXME: workaround for https://github.com/beeware/rubicon-objc/issues/228
        if toga.platform.current_platform == "iOS":
            import asyncio

            async def heartbeat(*args, **kwargs):
                while True:
                    await asyncio.sleep(0.0001)

            self.add_background_task(heartbeat)
        # END FIXME


def main():
    return Testbed(app_name="testbed")
