@echo off
rem pass --slow for slow execution
briefcase dev --app testbed --test -- tests/widgets/test_webview.py %*
