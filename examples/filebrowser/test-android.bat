@echo off
briefcase update android
echo.
if not "%errorlevel%"=="0" goto end

briefcase build android
echo.
if not "%errorlevel%"=="0" goto end
briefcase run android -d @beePhone
:end
