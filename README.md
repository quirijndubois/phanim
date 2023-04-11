# phanim
PHysics ANIMations: 

a bad Physics render engine

Look at the example files to figure out how to use the library.

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





