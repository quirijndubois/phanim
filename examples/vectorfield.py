from phanim import *
import numpy as np

screen = Screen(fullscreen=True,panning=True)
field = OldField(resolution=2,maxVectorScale=0.5)
particles = Particles()

nodes = Node(pos=[1,0]),Node(pos=[-1,0])

gravityStrength1 = 0.3
gravityStrength2 = -0.3

def update(screen):
    func = lambda x,y: (
        gravity([x,y],nodes[0].position,gravityStrength1) + gravity([x,y],nodes[1].position,gravityStrength2)
    )
    field.setField(func)

    screen.selected = findClosest([nodes[0].position,nodes[1].position],screen.mousePos)
    if distance(nodes[screen.selected].position,screen.mousePos) > 1:
        screen.selected = -1

    particles.area = screen.camera.bounds
    particles.lineWidth = 2*screen.camera.zoom/10
    particles.updatePosition(screen.dt,func)

def dragUpdate(screen):
    field.generateArrows()

screen.makeInteractive(nodes[0],nodes[1])
screen.play(makeGrid())
screen.play(Create(field,duration=120),Create(nodes[0],duration=120),Create(nodes[1],duration=120))
screen.play(*[Create(particle.trail) for particle in particles.particles])
screen.addUpdater(update)
screen.addMouseDragUpdater(dragUpdate)

screen.run()