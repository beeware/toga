# Positron

This is an example of an Electron-style "website as app" project using
[Positron](https://github.com/beeware/toga/blob/main/positron/README.md).

It serves a Django site called `webapp`, contained in `src/webapp`. The
contents of this folder are a stock version of what is produced by
`django-admin.py startproject`, collapsed into a single directory.

## Getting started

To set up a development environment:

```
$ python -m venv venv
$ ./venv/bin/activate
(venv) $ python -m pip install briefcase
```

To run Django management commands:

```
(venv) PYTHONPATH=src python src/manage.py
```

To run in development mode:

```
(venv) $ briefcase dev
```

To run as a packaged app:

```
(venv) $ briefcase run
```

The Django app will run on a SQLite3 database, stored in the user's data
directory (the location of this directory is platform specific). This
database file will be created if it doesn't exist, and migrations will
be run on every app start.

If you need to start the database with some initial content (e.g., an
initial user login) you can use `manage.py` to create an initial
database file. If there is a `db.sqlite3` in the
`src/positron/resources` folder when the app starts, and the user
doesn't already have a `db.sqlit3` file in their app data folder, the
initial database file will be copied into the user's data folder as a
starting point.

To create an initial database, use `manage.py` - e.g.,:

```
(venv) PYTHONPATH=src python src/manage.py migrate
(venv) PYTHONPATH=src python src/manage.py createsuperuser
```

This will create an initial `db.sqlite3` file with a superuser account.
All users of the app will have this superuser account in their database.
