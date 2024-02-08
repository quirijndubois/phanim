from phanim import *

s = Screen(fullscreen=True,zoom=10,grid=True,renderer="pygame",panning=False)

startPositions = [[0,1],[2,1],[4,1]]
startVelocities = [[0,0],[0,3],[0,6]]

slider = Slider(position=[0,-3.5],value=1,maxValue=2,color=color.red)

nodeRadius = 0.3

nodes = (
    Node(pos=startPositions[0],radius=nodeRadius),
    Node(pos=startPositions[1],vel=startVelocities[1],radius=nodeRadius,interactivityType="force"),
    Node(pos=startPositions[2],vel=startVelocities[2],radius=nodeRadius,interactivityType="force")
)
lines = (
    Line(start=startPositions[0],stop=startPositions[1],lineWidth=10),
    Line(start=startPositions[1],stop=startPositions[2],lineWidth=10),
)

trail = Trail(length=100,lineWidth=3)

C = 1e6
l = 2
G = 10

def update_physics(screen):
    dt = screen.dt * slider.value
    fz = [0,-G]
    spring01 = springForce(C,l,nodes[0].position,nodes[1].position)
    spring12 = springForce(C,l,nodes[1].position,nodes[2].position)
    spring21 = springForce(C,l,nodes[2].position,nodes[1].position)

    nodes[1].eulerODESolver(spring01+spring21+fz,dt)
    nodes[2].eulerODESolver(spring12+fz,dt)

def update(screen):
    lines[0].setEnds(nodes[0].position,nodes[1].position)
    lines[1].setEnds(nodes[1].position,nodes[2].position)
    trail.add(nodes[2].position,(255,150,100))

s.addUpdater(update_physics,substeps=50)
s.addUpdater(update)
s.play(laggedStart(
    Add(trail),
    *[Create(line) for line in lines],
    *[Create(node) for node in nodes],
    *[Create(phobject) for phobject in slider.groupObjects],
    )
)


s.makeInteractive(slider,nodes[1],nodes[2])

#s.wait(60)
#s.play(AnimateValue(lambda value: slider.setValue(value),[1,2]))
#s.wait(60)
#s.play(AnimateValue(lambda value: slider.setValue(value),[2,0.4]))
#s.wait(60)
#s.play(AnimateValue(lambda value: slider.setValue(value),[0.4,1.2]))
#s.play(AnimateValue(lambda value: slider.setValue(value),[1.2,1]))

s.run()
