# Setting up a development environment

{% extends "contribute/how/dev-environment.md" %}

{% block prerequisites_macos %}

You should also ensure you have the [macOS prerequisites][macos-prerequisites] installed.

{% endblock %}

{% block prerequisites_linux %}

You should also ensure you have the prerequisites for [GTK development][gtk-prerequisites] or the [Qt development][qt-prerequisites] installed.

{% endblock %}

{% block prerequisites_windows %}

You should also ensure you have the [Windows prerequisites][windows-prerequisites] installed.

{% endblock %}

{% block install_macos_tool %}

```console
(.venv) $ python -m pip install -e ./core -e ./dummy -e ./cocoa -e ./travertino --group dev
```

{% endblock %}

{% block install_linux_tool %}

```console
(.venv) $ python -m pip install -e ./core -e ./dummy -e ./gtk -e ./travertino --group dev
```

{% endblock %}

{% block install_windows_tool %}

```doscon
(.venv) C:\...>python -m  pip install -e ./core -e ./dummy -e ./winforms -e ./travertino --group dev
```

{% endblock %}
