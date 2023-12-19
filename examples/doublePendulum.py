from phanim import *
screen = Screen(fullscreen=True,zoom=15,panning=True)

startPositions = [[0,1],[2,1],[4,1]]
startVelocities = [[0,0],[0,3],[0,6]]
nodes = (
    Node(pos=startPositions[0]),
    Node(pos=startPositions[1],vel=startVelocities[1]),
    Node(pos=startPositions[2],vel=startVelocities[2])
)
lines = (
    Line(start=startPositions[0],stop=startPositions[1]),
    Line(start=startPositions[1],stop=startPositions[2]),
)

trail = Trail(length=1,lineWidth=3)

C = 10**5
l = 2
G = 10

def update_physics(screen):
    fz = [0,-G]
    spring01 = springForce(C,l,nodes[0].position,nodes[1].position)
    spring12 = springForce(C,l,nodes[1].position,nodes[2].position)
    spring21 = springForce(C,l,nodes[2].position,nodes[1].position)

    nodes[1].eulerODESolver(spring01+spring21+fz, screen.dt)
    nodes[2].eulerODESolver(spring12+fz, screen.dt)

def update(screen):
    lines[0].setEnds(nodes[0].position,nodes[1].position)
    lines[1].setEnds(nodes[1].position,nodes[2].position)
    trail.add(nodes[2].position,(255,150,100))
    screen.draw(trail)
    # screen.camera.position = nodes[2].position

screen.addUpdater(update_physics,substeps=20)
screen.addUpdater(update)

screen.play(Create(DGrid()))
screen.play(laggedStart(Create(lines[0]),Create(lines[1])))
screen.play(laggedStart(Create(nodes[0]),Create(nodes[1]),Create(nodes[2])))

screen.run()
