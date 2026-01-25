# Let's draw on a canvas!

One of the main capabilities needed to create many types of GUI applications is the ability to draw and manipulate lines, shapes, text, and other graphics. To do this in Toga, we use the Canvas Widget.

Utilizing the Canvas is as easy as determining the drawing operations you want to perform and then creating a new Canvas. All drawing objects that are created with one of the drawing operations are returned so that they can be modified or removed.

1. We first define the drawing operations we want to perform in a new function:

    ```python
    def draw_eyes(self):
	    with self.canvas.Fill(color=WHITE) as eye_whites:
		    eye_whites.arc(58, 92, 15)
			    eye_whites.arc(88, 92, 15, math.pi, 3 * math.pi)
    ```

    Notice that we also created and used a new fill state called `eye_whites`. The `with` keyword that is used for the fill operation causes everything draw using the state to be filled with a color. In this example we filled two circular eyes with the color white.

2. Next we create a new Canvas:

    ```python
    self.canvas = toga.Canvas(flex=1)
    ```

That's all there is to! In this example we also add our canvas to the `MainWindow` through use of the Box Widget:

```python
box = toga.Box(children=[self.canvas])
self.main_window.content = box
```

You'll also notice in the full example below that the drawing operations utilize states in addition to `Fill` including `state`, `ClosedPath`, and `Stroke`. This reduces the repetition of commands as well as groups drawing operations so that they can be modified together.

![image](images/tutorial-4.png)

Here's the source code

```python
-8<- "tutorial4/tutorial/app.py"
```

In this example, we see a new Toga widget - [`Canvas`][toga.Canvas].
