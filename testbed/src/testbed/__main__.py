if __package__ == "testbed":
    from testbed.app import main
elif __package__ == "testbed_qt":
    from testbed_qt.app import main


if __name__ == "__main__":
    main().main_loop()
