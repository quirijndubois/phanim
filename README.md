![phanim logo](https://github.com/quirijndaboyy/phanim/blob/main/phanim/icon.png)

PHysics ANIMations: 
a bad Physics render library

The project is still in the early stages of development, so larger simulation will be slow and features are very limited. Look at the example files to see what cool things you can already do!

## Requirements
pygame, numpy

## Installation
Clone the repository and put your own files in the base folder. Now simply:

```python
import phanim
```

## Usage

After importing you can create a phanim screen as follows:

```python
resolution = [400,400] #Or any other resolution you require.
myScreen = phanim.Screen(resolution)

```
Now we can create something to render on the screen. In this example we will create a simple grid, but the possibilities are endless.

```python
grid = phanim.Grid(1,1,10,10) #This creates a grid with each line seperated by 1, and 10 lines to each side of the origin.
```

Now we can define a update function that will be called each frame. Then we add the update function to the manim updater list.

```python
def updateFunction(screen):
  screen.draw(grid)
  
myScreen.addUpdater(updateFunction)
```
Now we can run the script and a window with a simple grid should show up.

```python
myScreen.run()
```
We can also create different object. For example, a blue arrow, which points to the position of the cursor at all times.
We can create the arrow by defining it like this:

```python
arrow = phanim.Arrow(color="blue")
```
We must draw it withing the update function. This can be done by either altering our first update function, or creating a new one. In this example we will create a new update function.

```python
def drawArrow(screen):
  arrow.setDirection([0,0],screen.mousePos)
  screen.draw(arrow)
```
Then add this function to the updater list and run the script:

```python
myScreen.addUpdater(drawArrow)
myScreen.run()
```
The final script will look like this:

```python
import phanim

myScreen = phanim.Screen([400,400])
grid = phanim.Grid(1,1,10,10)
arrow = phanim.Arrow(color="blue")

def updateFunction(screen):
  screen.draw(grid)
  
def drawArrow(screen):
  arrow.setDirection([0,0],screen.mousePos)
  screen.draw(arrow)

myScreen.addUpdater(updateFunction)
myScreen.addUpdater(drawArrow)
myScreen.run()
```



## Examples

A simple visualisation of the electric field can be found in examples/vectorField.py
![vector field](https://github.com/quirijndaboyy/phanim/blob/main/gifs/vectorFIeld.gif)

A simulation of a triple pendulum with the use of stiff springs can be found in examples/triplePendulum.py. The graphs on the right show the energy that each of the masses has. The yellow graph shows the total energy in the system.
![triple pendulum](https://github.com/quirijndaboyy/phanim/blob/main/gifs/pendulum.gif)

Or just a simple double pendulum(looks better imo):
![double pendulum](https://github.com/quirijndaboyy/phanim/blob/main/gifs/double_pendulum.gif)




