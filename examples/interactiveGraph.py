from phanim import *

s = Screen(fullscreen=True,panning=True)

graph = RandomGraph(15,chance=0.17)

s.add(DGrid(n_horizontal=100,n_vertical=100))
s.play(Create(graph))
s.makeInteractive(graph)
s.addUpdater(lambda s: graph.update(s.dt))
s.run()