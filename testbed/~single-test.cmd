@echo off
rem pass --slow for slow execution
briefcase dev --test -- tests/widgets/test_webview.py %*
