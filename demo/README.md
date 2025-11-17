# Toga Demo

A demonstration of the capabilities of the [Toga widget toolkit](https://beeware.org/toga).

# Quickstart

For details of Toga's pre-requisites, see the [Toga project on GitHub](https://github.com/beeware/toga).

Once those pre-requisites have been met, in your virtualenv, install Toga Demo, and then run it:

```console
$ pip install toga-demo
$ toga-demo
```

This will pop up a GUI window.

If you have cloned the toga repository, install the dependent packages in your virtualenv:

```console
$ cd toga
$ pip install -e ./core
```

Then install the platform specific code:

```console
$ pip install -e ./cocoa      # macOS
$ pip install -e ./gtk        # Linux
$ pip install -e ./winforms   # Windows
```

Finally navigate to the demo directory and run the application:

```
$ cd demo
$ python -m toga_demo
```

# Community

Toga Demo is part of the [BeeWare suite](https://beeware.org). You can talk to the community through:

- [@beeware@fosstodon.org on Mastodon](https://fosstodon.org/@beeware)
- [Discord](https://beeware.org/bee/chat/)
- The Toga [GitHub Discussions forum](https://github.com/beeware/toga/discussions)

We foster a welcoming and respectful community as described in our [BeeWare Community Code of Conduct](https://beeware.org/community/behavior/).

# Contributing

If you experience problems with Toga, [log them on GitHub](https://github.com/beeware/toga/issues).

If you'd like to contribute to Toga development, our [contribution guide](https://toga.beeware.org/en/latest/how-to/contribute/) details how to set up a development environment, and other requirements we have as part of our contribution process.
