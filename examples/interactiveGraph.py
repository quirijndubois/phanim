from phanim import *

s = Screen(fullscreen=True,grid=True,panning=True,renderer="pygame")

slider = Slider(position=[-3,2],minValue=0.05,maxValue=2)
s.makeInteractive(slider)
def updateK(s):
    graph.k = slider.value
s.addUpdater(updateK)

#graph of the dutch provinces
graph = Graph(12,
    [    [0, 1], [0, 2], 
        [1, 2], [1, 3], 
        [2, 3], [2, 5], 
        [3, 4], [3, 5], 
        [4, 5], [4, 6], [4, 7], 
        [5, 6], [5, 8], [5, 10], 
        [6, 7], [6, 8], 
        [7, 8], 
        [8, 9], [8, 10], 
        [9, 10], 
        [10, 11]
    ]
)
#or just make a random graph
graph = RandomGraph(15,chance=0.17)


s.play(Create(graph))
s.makeInteractive(graph)
s.addUpdater(lambda s: graph.update(s.dt))
s.play(Create(slider))
s.run()