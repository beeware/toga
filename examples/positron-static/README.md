# Positron

This is an example of an Electron-style "website as app" project using
[Positron](https://github.com/beeware/toga/blob/main/positron/README.md).

It serves a static site from the `src/positron/resources/webapp` folder.

## Getting started

To set up a development environment:

```
$ python -m venv venv
$ ./venv/bin/activate
(venv) $ python -m pip install briefcase
```

To run in development mode:

```
(venv) $ briefcase dev
```

To run as a packaged app:

```
(venv) $ briefcase run
```
