First import the library with:
```python
from phanim import *
```

After importing you can create a phanim screen as follows:

```python
myScreen = phanim.Screen()
```
This will use the device screen resolution. We can also change some of the screen parameters.
```python
myScreen = phanim.Screen(fullscreen=False,resolution=(1920,1080))
```

Now we can create something to render on the screen. In this example we will create a simple grid, but the possibilities are endless.

```python
grid = phanim.Grid(1,1,10,10) #This creates a grid with each line seperated by 1, and 10 lines to each side of the origin.
```

Now we can add some wait time and animate the grid being added to the screen by:

```python
myScreen.wait(60) #This will add an empty animation for 60 frames or 1 seconds.
myScreen.play(Create(grid))
```
Now we can run the script and a window with a simple grid should show up.

```python
myScreen.run()
```
We can also create different object. For example, a blue arrow, which points to the position of the cursor at all times.
We can create the arrow by defining it like this:

```python
arrow = phanim.Arrow(color=color.blue)
```
Now we will create an update function that will be called each frame and move the end of the arrow to the cursor.

```python
def setArrow(screen):
  arrow.setDirection([0,0],screen.mousePos)
```

Then add this function to the updater list and run the script:

```python
myScreen.addUpdater(setArrow)
myScreen.play(Create(arrow))
myScreen.run()
```
Make sure you only add the .run() command once at the very end of your script. We can also add some dotted lines to track the mouse position like this:

```python
lines = DottedLine(),DottedLine()

def setLines(screen):
    lines[0].setEnds([screen.mousePos[0],0],screen.mousePos)
    lines[1].setEnds([0,screen.mousePos[1]],screen.mousePos)

myScreen.play(Create(lines[0]),Create(lines[1]))
myScreen.addUpdater(setLines)
```

After combining the update functions the final script will look like this:

```python
from phanim import *

myScreen = Screen(fullscreen=True)

grid = Grid(1,1,10,10)
arrow =Arrow(color=color.blue)
lines = DottedLine(),DottedLine()

def update(screen):
  arrow.setDirection([0,0],screen.mousePos)
  lines[0].setEnds([screen.mousePos[0],0],screen.mousePos)
  lines[1].setEnds([0,screen.mousePos[1]],screen.mousePos)

myScreen.addUpdater(update)

myScreen.wait(60)
myScreen.play(Create(grid))
myScreen.play(Create(arrow))
myScreen.play(Create(lines[0]),Create(lines[1]))

myScreen.run()
```