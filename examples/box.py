from phanim import *
import numpy as np

circle = Circle(color=color.green,radius=1)
box = Rectangle(width=8,height=4,color=color.blue)

node = Node(pos=[-1,0],vel=[3,4])
trail = Trail(lineWidth=10)

arrow = Arrow()

def updateNode(screen):
    if screen.t > 4:
        node.eulerODESolver([0,-3], screen.dt)
        if node.position[1] < -2 + node.radius or node.position[1] > 2 - node.radius:
            node.velocity[1] *= -1
        if node.position[0] < -4 + node.radius or node.position[0] > 4 - node.radius:
            node.velocity[0] *= -1

def updateCamera(screen):
    if screen.t > 10:
        t = (screen.t-10)/5
        tnew = interp(t**2,t**0.5,t)
        screen.camera.setPosition(interp2d([0,0],node.position,tnew))
    if screen.t > 15:
        screen.camera.setPosition(node.position)

screen = Screen([1360,765],zoom=11)

screen.wait(60)
screen.play(Create(circle))
screen.play()
screen.play(Transform(circle,box,duration=120),Create(DGrid()))
screen.play(Remove(circle),Add(circle))
screen.play(Add(trail))
screen.play(Create(node))
screen.wait(60*10)
screen.play(AnimateValue(screen.camera.setZoom,[11,5],duration=180))
screen.play(Create(arrow))

screen.addUpdater(updateNode,substeps=100)
screen.addUpdater(lambda s: trail.add(node.position,color.blue))
screen.addUpdater(updateCamera)
screen.addUpdater(lambda s: arrow.setDirection(node.position,np.array(node.velocity)/6))
screen.run()