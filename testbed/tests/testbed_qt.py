from .testbed import main

if __name__ == "__main__":
    import testbed_qt.app

    main(testbed_qt.app, backend_override="toga_qt")
