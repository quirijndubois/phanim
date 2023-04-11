![phanim](https://github.com/quirijndaboyy/phanim/blob/main/phanim/icon.png =250x)

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
resolution = [1000,1000] #Or any other resolution you require.
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

```
myScreen.run()
```

## Examples

A simple visualisation of the electric field can be found in examples/vectorField.py
![vector field](https://github.com/quirijndaboyy/phanim/blob/main/gifs/vectorFIeld.gif)

A simulation of a triple pendulum with the use of stiff springs can be found in examples/triplePendulum.py. The graphs on the right show the energy that each of the masses has. The yellow graph shows the total energy in the system.
![triple pendulum](https://github.com/quirijndaboyy/phanim/blob/main/gifs/pendulum.gif)

Or just a simple double pendulum(looks better imo):
![double pendulum](https://github.com/quirijndaboyy/phanim/blob/main/gifs/double_pendulum.gif)




