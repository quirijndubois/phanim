from phanim import *
import numpy as np

s = Screen(zoom=9, panning=False, grid=False)

slider = Slider(position=[0, 3.5], maxValue=np.sqrt(3))

nodes = [
    Node(pos=[1, 1], vel=[0, 0], borderColor=color.red),
    Node(pos=[2, -2], vel=[-1, 4], borderColor=color.green),
    Node(pos=[0, 0], vel=[-1, -2], borderColor=color.blue)
]
trails = [
    Trail(length=50),
    Trail(length=50),
    Trail(length=50),
]


def update(s):
    G = 15
    dt = s.dt*(slider.value**2)
    dist = 0.01
    if magSquared(nodes[0].position-nodes[1].position) > dist:
        toggle01 = 1
    else:
        toggle01 = 0

    if magSquared(nodes[1].position-nodes[2].position) > dist:
        toggle12 = 1
    else:
        toggle12 = 0

    if magSquared(nodes[2].position-nodes[0].position) > dist:
        toggle20 = 1
    else:
        toggle20 = 0

    nodes[0].eulerODESolver(
        gravity(nodes[0].position, nodes[1].position, G*nodes[0].mass*nodes[1].mass)*toggle01 +
        gravity(nodes[0].position, nodes[2].position, G *
                nodes[0].mass*nodes[2].mass)*toggle20, dt
    )
    nodes[1].eulerODESolver(
        gravity(nodes[1].position, nodes[0].position, G*nodes[0].mass*nodes[1].mass)*toggle01 +
        gravity(nodes[1].position, nodes[2].position, G *
                nodes[1].mass*nodes[2].mass)*toggle12, dt
    )
    nodes[2].eulerODESolver(
        gravity(nodes[2].position, nodes[0].position, G*nodes[0].mass*nodes[2].mass)*toggle20 +
        gravity(nodes[2].position, nodes[1].position, G *
                nodes[2].mass*nodes[1].mass)*toggle12, dt
    )

    for node in nodes:
        # if abs(node.position[0])>s.camera.bounds[0][1] or abs(node.position[1])>s.camera.bounds[1][1]:
        bounds = [
            [-7, 7],
            [-4, 3]
        ]
        e = 0.05
        if node.position[0] > bounds[0][1]-node.radius:
            node.velocity[0] *= -1
            node.position[0] = bounds[0][1]-node.radius-e
        elif node.position[0] < bounds[0][0]+node.radius:
            node.velocity[0] *= -1
            node.position[0] = bounds[0][0]+node.radius+e
        elif node.position[1] > bounds[1][1]-node.radius:
            node.velocity[1] *= -1
            node.position[1] = bounds[1][1]-node.radius-e
        elif node.position[1] < bounds[1][0]+node.radius:
            node.velocity[1] *= -1
            node.position[1] = bounds[1][0]+node.radius+e


def frameUpdate(s):
    # s.camera.setPosition(nodes[2].position)
    trails[0].add(nodes[0].position, nodes[0].borderColor)
    trails[1].add(nodes[1].position, nodes[1].borderColor)
    trails[2].add(nodes[2].position, nodes[2].borderColor)


circle = Circle(color=color.red)
rectangle = Rectangle(width=14, height=7, position=[0, -.5])

s.addUpdater(update, substeps=100)
s.addUpdater(frameUpdate)

s.play(Create(circle))
s.play(laggedStart(
    Transform(circle, rectangle),
    *[Create(trail) for trail in trails],
    *[Create(node) for node in nodes],
    Create(slider.groupObjects[0]),
    Create(slider.groupObjects[1]),
    lagRatio=0.5
))

s.makeInteractive(slider, *nodes)


s.run()
