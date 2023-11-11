![phanim logo](https://github.com/quirijndaboyy/phanim/blob/main/phanim/icon.png)

PHysics ANIMations: 
a (quite bad) Physics render library

The project is still in the early stages of development, so larger simulation will be slow and features are very limited. Look at the example files to see what cool things you can already do!

## Examples

A simple visualisation of the electric field can be found in examples/vectorField.py
![vector field](https://github.com/quirijndaboyy/phanim/blob/main/gifs/vectorFIeld.gif)

A simulation of a triple pendulum with the use of stiff springs can be found in examples/triplePendulum.py. The graphs on the right show the energy that each of the masses has. The yellow graph shows the total energy in the system.
![triple pendulum](https://github.com/quirijndaboyy/phanim/blob/main/gifs/pendulum.gif)

Or just a simple double pendulum(looks better imo):
![double pendulum](https://github.com/quirijndaboyy/phanim/blob/main/gifs/double_pendulum.gif)

## Requirements
To install the requirements run the following command:
```
pip install -r requirements.txt
```

## Installation
Clone the repository and put your own files in the base folder. Now simply:

```python
from phanim import *
```

## Usage

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
myScreen.wait(120) #This will add an empty animation for 120 frames or 2 seconds.
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
def drawArrow(screen):
  arrow.setDirection([0,0],screen.mousePos)
```

Then add this function to the updater list and run the script:

```python
myScreen.addUpdater(drawArrow)
myScreen.play(Create(arrow))
myScreen.run()
```
We can also add some dotted lines to track the mouse position like this:

```python
lines = phanim.dottedLine(lineWidth=1),phanim.dottedLine(lineWidth=1)

def drawLines(screen):
    lines[0].setEnds([screen.mousePos[0],0],screen.mousePos)
    lines[1].setEnds([0,screen.mousePos[1]],screen.mousePos)
myScreen.addUpdater(drawLines)
```

After combining the update functions the final script will look like this:

```python

```








