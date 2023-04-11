import phanim as p
import numpy as np

size = 0.7
screen = p.Screen([1920*size,1080*size])

grids = p.Grid(0.5,0.5,20,20,color=(30,30,30)),p.Grid(1, 1, 10, 10)
graph = p.Graph(xSize=[-4,4],ySize=[-2,2])


def update(screen):

    x = np.linspace(screen.t-10,screen.t,1000)
    y = np.sin(x) + np.cos(x*np.pi) + x/np.e

    graph.setData(y)
    screen.draw(*grids)
    screen.draw(graph)

screen.addUpdater(update)
screen.run()
