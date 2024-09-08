from phanim import *
import numpy as np

grid = Grid(1, 1, 10, 10)
axes = Axes(xRange=[-2, 7], yRange=[-1, 4], showNumbers=False)

graph = PlotGraph(strokeWidth=0.03, color=(150, 150, 255))
graph2 = PlotGraph(strokeWidth=0.03, color=(255, 150, 150))
x = np.linspace(-3, 10, 500)
graph.setData(x, np.sin(x))
graph2.setData(x, x**2/10)

scr = Screen(grid=False, fontSize=0.3)
scr.camera.setPosition([2.5, 1.5])

scr.play(Create(grid))
scr.play(Create(axes))
scr.play(Create(graph))
scr.play(Transform(graph, graph2))
scr.wait(120)
scr.play(Destroy(graph), Destroy(axes, duration=120),
         Destroy(grid, duration=240))

scr.run()
