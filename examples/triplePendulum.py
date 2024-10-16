from phanim import *
import numpy as np

drawVectors = True
drawTrails = True

screen = Screen(zoom=12, fontSize=0.4)

trails = [
    Trail(color=color.red),
    Trail(color=color.green),
    Trail(color=color.blue, lineWidth=3, length=50),
]

graphs = [
    LiveGraph(pos=[3, 2], xSize=[-2, 2], color=color.red, liveRange=100),
    LiveGraph(pos=[3, 0], xSize=[-2, 2], color=color.green, liveRange=100),
    LiveGraph(pos=[3, -2], xSize=[-2, 2], color=color.blue, liveRange=100),
    LiveGraph(pos=[-3.5, 2], xSize=[-2, 2], color=color.yellow, liveRange=100),
]

nodes = [
    Node(pos=[0, 1], radius=0.4, vel=[0, 0], interactivityType="force"),
    Node(pos=[0, 3], radius=0.4, vel=[0.22, 0], interactivityType="force"),
    Node(pos=[0, 5], radius=0.4, vel=[0, 0], interactivityType="force"),
    Node(pos=[0, 7], radius=0.4, vel=[-0.2, 0], interactivityType="force"),
]

lines = [
    Line(begin=nodes[0].position, end=nodes[1].position),
    Line(begin=nodes[1].position, end=nodes[2].position),
    Line(begin=nodes[2].position, end=nodes[3].position),
]

arrows = [
    Arrow(color=color.red),
    Arrow(color=color.green),
    Arrow(color=color.blue),
]

substeps = 50
C = 10**6
l1 = 2
l2 = 2
l3 = 2
g = 3


def update_physics(screen):
    if screen.t > 0.3:

        fz1 = [0, -nodes[1].mass * g]
        fz2 = [0, -nodes[2].mass * g]
        fz3 = [0, -nodes[3].mass * g]

        force01 = springForce(C, l1, nodes[0].position, nodes[1].position)
        force12 = springForce(C, l2, nodes[1].position, nodes[2].position)
        force21 = springForce(C, l2, nodes[2].position, nodes[1].position)
        forcemouse = springForce(
            10, 0, screen.LocalCursorPosition, nodes[2].position)*0

        force23 = springForce(C, l3, nodes[2].position, nodes[3].position)
        force32 = springForce(C, l3, nodes[3].position, nodes[2].position)

        force1 = force01+fz1+force21
        force2 = force12+fz2+force32
        force3 = force23+fz3

        nodes[1].eulerODESolver(force1, screen.dt)
        nodes[2].eulerODESolver(force2, screen.dt)
        nodes[3].eulerODESolver(force3, screen.dt)


def update_screen(screen):
    arrows[0].setDirection(nodes[1].position, nodes[1].velocity, scale=0.2)
    arrows[1].setDirection(nodes[2].position, nodes[2].velocity, scale=0.2)
    arrows[2].setDirection(nodes[3].position, nodes[3].velocity, scale=0.2)

    trails[0].add(nodes[1].position, (255, 0, 0, 255))
    trails[1].add(nodes[2].position, (0, 255, 0, 255))
    trails[2].add(nodes[3].position, (0, 0, 255, 255))

    # kinetic1 = 0.5 * nodes[1].mass * magnitude(nodes[1].velocity)**2
    # kinetic2 = 0.5 * nodes[2].mass * magnitude(nodes[2].velocity)**2
    # kinetic3 = 0.5 * nodes[3].mass * magnitude(nodes[3].velocity)**2

    # potential1 = nodes[1].mass * g * nodes[1].position[1]
    # potential2 = nodes[2].mass * g * nodes[2].position[1]
    # potential3 = nodes[3].mass * g * nodes[3].position[1]

    # energy1 = kinetic1+potential1
    # energy2 = kinetic2+potential2
    # energy3 = kinetic3+potential3
    # energy = energy1+energy2+energy3

    # graphs[0].addDataPoint(energy1)
    # graphs[1].addDataPoint(energy2)
    # graphs[2].addDataPoint(energy3)
    # graphs[3].addDataPoint(energy)

    # screen.lastEnergy = energy


screen.addUpdater(update_physics, substeps=substeps)
screen.addUpdater(update_screen)

screen.makeInteractive(*nodes)

# [screen.add(graph) for graph in graphs]
if drawTrails:
    [screen.add(trail) for trail in trails]
if drawVectors:
    [screen.add(arrow) for arrow in arrows]

screen.play(laggedStart(*[Create(line) for line in lines],
            *[Create(node) for node in nodes], lagRatio=0.5))

screen.makeInteractive(nodes[2])

screen.run()
