from phanim import *

s = Screen(expand_grid=False)

# we make the graph of a cube
graph = SoftBody(
    [
        [1, 1],
        [-1, 1],
        [-1, -1],
        [1, -1],
    ],
    [
        [0, 1],
        [1, 2],
        [2, 3],
        [3, 0],
        [0, 2],
    ],
)

s.makeInteractive(graph)

s.play(Add(graph))

s.addUpdater(graph.update, substeps=100)

s.run()
