import toga


class SubclassedApp(toga.App):
    pass


def main():
    app = SubclassedApp("Subclassed App", "org.testbed.subclassed-app")

    print(f"app.paths.app={app.paths.app.resolve()}")
    print(f"app.paths.config={app.paths.config.resolve()}")
    print(f"app.paths.data={app.paths.data.resolve()}")
    print(f"app.paths.cache={app.paths.cache.resolve()}")
    print(f"app.paths.logs={app.paths.logs.resolve()}")
    print(f"app.paths.toga={app.paths.toga.resolve()}")


if __name__ == "__main__":
    main()
