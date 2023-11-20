from phanim import *

s = Screen(fullscreen=True,panning=True)

graph = RandomGraph(15,chance=0.2)

s.play(makeGrid())
s.play(Create(graph))
s.makeInteractive(graph)
s.addUpdater(lambda s: graph.update(s.dt))
s.run()