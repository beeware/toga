@echo off
rem pass --slow for slow execution
briefcase run android --app testbed --test -r -- tests/widgets/test_webview.py %*
