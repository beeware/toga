from rubicon.java import JavaClass, JavaInterface

# The Android cookiecutter template creates an app whose main Activity is
# called `MainActivity`. The activity assumes that we will store a reference
# to an implementation/subclass of `IPythonApp` in it.
MainActivity = JavaClass('org/beeware/android/MainActivity')


# The `IPythonApp` interface in Java allows Python code to
# run on Android activity lifecycle hooks such as `onCreate()`.
IPythonApp = JavaInterface('org/beeware/android/IPythonApp')
