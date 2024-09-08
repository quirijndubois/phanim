![phanim logo](https://github.com/quirijndaboyy/phanim/blob/main/src/phanim/icon.png)

PHysics ANIMations: 
a (quite bad) Physics render library

The project is still in the early stages of development, so larger simulations will be slow and features are limited. Look at the example files to see what cool things you can already do!

Take a look at the [documentation](https://quirijndubois.github.io/phanim/) for an in depth look!

## Examples

A simple visualisation of the electric field can be found in examples/vectorField.py
![vector field](https://github.com/quirijndaboyy/phanim/blob/main/gifs/vectorFIeld.gif)

A simulation of a triple pendulum with the use of stiff springs can be found in examples/triplePendulum.py. The graphs on the right show the energy that each of the masses has. The yellow graph shows the total energy in the system.
![triple pendulum](https://github.com/quirijndaboyy/phanim/blob/main/gifs/pendulum.gif)

Or just a simple double pendulum(looks better imo):
![double pendulum](https://github.com/quirijndaboyy/phanim/blob/main/gifs/pendulum_compressed.mp4)


## Installation
Install with pip (old shitty version):
```bash
pip install phanim
``` 
If you want to use the very latest version you can also clone the repository and import the phanim folder within python.

You can also install phanim systemwide with pip from this repo by doing the following:
```bash
git clone https://github.com/quirijndubois/phanim
```
```bash
cd phanim
```
```bash
pip install -e .
```

## Usage

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
  arrow.setDirection([0,0],screen.LocalCursorPosition)
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
    lines[0].setEnds([screen.LocalCursorPosition[0],0],screen.LocalCursorPosition)
    lines[1].setEnds([0,screen.LocalCursorPosition[1]],screen.LocalCursorPosition)

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
  arrow.setDirection([0,0],screen.LocalCursorPosition)
  lines[0].setEnds([screen.LocalCursorPosition[0],0],screen.LocalCursorPosition)
  lines[1].setEnds([0,screen.LocalCursorPosition[1]],screen.LocalCursorPosition)

myScreen.addUpdater(update)

myScreen.wait(60)
myScreen.play(Create(grid))
myScreen.play(Create(arrow))
myScreen.play(Create(lines[0]),Create(lines[1]))

myScreen.run()
```

## Recording

Phanim also has built in recording functionality. Keep in mind that this will impact real-time performance significantly. Luckily recordings are independent from the real time frame rate. This is the same for simulations that use screen.dt. Recordings can be turned on by passing an argument to the Screen:

```python
s = Screen(record=True)
...
s.run()
```
or if you want more options:
```python
s = Screen(record=True,recording_output="recording.mp4",recording_fps=30)
...
s.run()
```
