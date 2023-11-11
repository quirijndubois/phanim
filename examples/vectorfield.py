#WARNING! very slow! Should be radically optimized

from phanim import *
import numpy as np

screen = Screen(fullscreen=True)
grids = Grid(0.25,0.25,20,20,color=(30,30,30)),Grid(0.5,0.5,10,10)
field = Field(resolution=2,maxVectorScale=0.4)

particles = Particles(radius=0,speed=10,n=500,lifetime=10)

nodes = Node(pos=[1,0]),Node(pos=[-1,0])

gravityStrength1 = 0.3
gravityStrength2 = -0.3
swirlSrength1 = 0
swirlSrength2 = 0


def update(screen):
    func = lambda x,y: (
        gravity([x,y],nodes[0].position,gravityStrength1) + gravity([x,y],nodes[1].position,gravityStrength2) +
        swirlForce([x,y],nodes[0].position,swirlSrength1) + swirlForce([x,y],nodes[1].position,swirlSrength2)
    )

    screen.selected = findClosest([nodes[0].position,nodes[1].position],screen.mousePos)
    if distance(nodes[screen.selected].position,screen.mousePos) > 1:
        screen.selected = -1

    field.setField(func)
    field.generateArrows()

    particles.setVelocity(func)
    particles.updatePosition(screen.dt)

    screen.draw(*grids)
    screen.draw(*field.arrows)
    for particle in particles.particles:
        screen.draw(particle.trail)
        pass
def dragFunction(screen):
    if screen.selected != -1:
        nodes[screen.selected].setPosition(screen.mousePos)

screen.play(Create(nodes[0]),Create(nodes[1]))
screen.addUpdater(update)
screen.addMouseDragUpdater(dragFunction)

screen.run()