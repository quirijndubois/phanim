import phanim
import numpy as np

screen = phanim.Screen((1600,900))
grids = phanim.Grid(0.25,0.25,20,20,color=(30,30,30)),phanim.Grid(0.5,0.5,10,10)
field = phanim.Field(resolution=2,maxVectorScale=0.4)

particles = phanim.Particles(radius=0,speed=10,n=500,lifetime=10)

nodes = phanim.Node(pos=[1,0]),phanim.Node(pos=[-1,0])

gravityStrength1 = 0.3
gravityStrength2 = -0.3
swirlSrength1 = 0
swirlSrength2 = 0


def update(screen):
    func = lambda x,y: (
        phanim.gravity([x,y],nodes[0].position,gravityStrength1) + phanim.gravity([x,y],nodes[1].position,gravityStrength2) +
        phanim.swirlForce([x,y],nodes[0].position,swirlSrength1) + phanim.swirlForce([x,y],nodes[1].position,swirlSrength2)
    )

    screen.selected = phanim.findClosest([nodes[0].position,nodes[1].position],screen.mousePos)
    if phanim.distance(nodes[screen.selected].position,screen.mousePos) > 1:
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
    screen.draw(*nodes)

def dragFunction(screen):
    if screen.selected != -1:
        nodes[screen.selected].setPosition(screen.mousePos)

screen.addUpdater(update)
screen.addMouseDragUpdater(dragFunction)

screen.run()