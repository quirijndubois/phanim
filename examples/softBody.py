from phanim import *

s = Screen()

graph1 = SoftBody(
    np.array([
        [-1, 1], [0, 1], [1, 1],
        [-1, 0], [0, 0], [1, 0],
        [-1, -1], [0, -1], [1, -1],
    ])+np.array([[3, 1.5]]*9),
    [
        [0, 1],
        [1, 2],
        [3, 4],
        [4, 5],
        [6, 7],
        [7, 8],
        [0, 3],
        [1, 4],
        [2, 5],
        [3, 6],
        [4, 7],
        [5, 8],
        [0, 4],
        [1, 5],
        [3, 7],
        [4, 8],
        [2, 4],
        [4, 6],
        [1, 3],
        [5, 7],
    ],
    springConstant=5e3,
    dampingConstant=10,
    hull=[0, 1, 2, 5, 8, 7, 6, 3, 0]
)
graph2 = SoftBody(
    np.array([
        [-1, 1], [0, 1], [1, 1],
        [-1, 0], [0, 0], [1, 0],
        [-1, -1], [0, -1], [1, -1],
    ])+np.array([[-3, 1.5]]*9),
    [
        [0, 1],
        [1, 2],
        [3, 4],
        [4, 5],
        [6, 7],
        [7, 8],
        [0, 3],
        [1, 4],
        [2, 5],
        [3, 6],
        [4, 7],
        [5, 8],
        [0, 4],
        [1, 5],
        [3, 7],
        [4, 8],
        [2, 4],
        [4, 6],
        [1, 3],
        [5, 7],
    ],
)

s.makeInteractive(graph1)
s.makeInteractive(graph2)

floorheight = -2
floor = Line(
    begin=[s.camera.bounds[0][0], floorheight],
    end=[s.camera.bounds[0][1], floorheight], lineWidth=2)


s.play(Create(floor))
s.play(Add(graph1))
s.play(Create(graph2))


def updatePhysics(s):
    if s.t < 3.5:
        return

    graph1.update(s)
    graph2.update(s)

    for i in range(graph1.vertices):
        if graph1.positions[i][1] < floorheight:
            graph1.positions[i][1] = floorheight + .01
            graph1.velocities[i][0] *= 0
            graph1.velocities[i][1] *= 0

        if graph1.positions[i][0] < s.camera.bounds[0][0]:
            graph1.positions[i][0] = s.camera.bounds[0][0] + .01
            graph1.velocities[i][0] *= 0
            graph1.velocities[i][1] *= 0

        if graph1.positions[i][0] > s.camera.bounds[0][1]:
            graph1.positions[i][0] = s.camera.bounds[0][1] - .01
            graph1.velocities[i][0] *= 0
            graph1.velocities[i][1] *= 0

        if graph1.positions[i][1] > s.camera.bounds[1][1]:
            graph1.positions[i][1] = s.camera.bounds[1][1] - .01
            graph1.velocities[i][0] *= 0
            graph1.velocities[i][1] *= 0

    for i in range(graph2.vertices):
        if graph2.positions[i][1] < floorheight:
            graph2.positions[i][1] = floorheight + .01
            graph2.velocities[i][1] *= 0
            graph2.velocities[i][0] *= 0

        if graph2.positions[i][0] < s.camera.bounds[0][0]:
            graph2.positions[i][0] = s.camera.bounds[0][0] + .01
            graph2.velocities[i][0] *= 0
            graph2.velocities[i][1] *= 0

        if graph2.positions[i][0] > s.camera.bounds[0][1]:
            graph2.positions[i][0] = s.camera.bounds[0][1] - .01
            graph2.velocities[i][0] *= 0
            graph2.velocities[i][1] *= 0

        if graph2.positions[i][1] > s.camera.bounds[1][1]:
            graph2.positions[i][1] = s.camera.bounds[1][1] - .01
            graph2.velocities[i][0] *= 0
            graph2.velocities[i][1] *= 0


def update(s):
    floor.setEnds(
        [s.camera.bounds[0][0], floorheight],
        [s.camera.bounds[0][1], floorheight],
    )


s.addUpdater(update)
s.addUpdater(updatePhysics, substeps=10)


s.run()
