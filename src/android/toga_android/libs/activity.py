from rubicon.java import JavaClass, JavaInterface

# The Android cookiecutter template creates an app whose main Activity is
# called `MainActivity`. The activity assumes that we will store a reference
# to an implementation/subclass of `IPythonApp` in it.
MainActivity = JavaClass('org/beeware/android/MainActivity')

# The `IPythonApp` interface in Java allows Python code to
# run on Android activity lifecycle hooks such as `onCreate()`.
IPythonApp = JavaInterface('org/beeware/android/IPythonApp')

# The `DrawHandlerView` Java class is an `android.view.View`. It allows user
# code to draw on its canvas.
#
# After a `DrawHandlerView` is constructed, you must provide a draw handler
# with `setDrawHandler()`. Whenever Android calls the `DrawHandlerView`'s `onDraw()`,
# the draw handler view will call the draw handler's `handleDraw()` with the
# `android.graphics.Canvas`.
DrawHandlerView = JavaClass('org/beeware/android/DrawHandlerView')
IDrawHandler = JavaInterface('org/beeware/android/IDrawHandler')
