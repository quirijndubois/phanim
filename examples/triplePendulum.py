import phanim
import numpy as np

drawVectors = False
drawTrails = True

screensize = 0.7
screen = phanim.Screen([1600,900],zoom=18,fontSize=0.4)

grid1 = phanim.Grid(1,1,10,10)
grid2 = phanim.Grid(0.5,0.5,20,20,color=(30,30,30))

trail1 = phanim.Trail(color="red")
trail2 = phanim.Trail(color="green")
trail3 = phanim.Trail(color="blue",lineWidth=3,length=150)

graph1 = phanim.Graph(pos=[5,3],xSize=[-2,2],color="red")
graph2 = phanim.Graph(pos=[5,0],xSize=[-2,2],color="green")
graph3 = phanim.Graph(pos=[5,-3],xSize=[-2,2],color="blue")
graph4 = phanim.Graph(pos=[-6,3],xSize=[-2,2],color="yellow")

node0 = phanim.Node(pos=[-2,1],radius=0.2)
node1 = phanim.Node(pos=[-2,3],radius=0.2)
node2 = phanim.Node(pos=[-2,5],radius=0.2)
node3 = phanim.Node(pos=[-2,7],radius=0.2)

node1.velocity = [0.22,0]
node3.velocity = [-0.2,0]

arrow1 = phanim.Arrow(color="red")
arrow2 = phanim.Arrow(color="green")
arrow3 = phanim.Arrow(color="blue")

substeps = 100
C = 10**7
l1 = 2
l2 = 2
l3 = 2
g = 3
screen.lastEnergy = 0

def update_physics(screen):
    if screen.t > 0.3:

        fz1 = [0,-node1.mass * g]
        fz2 = [0,-node2.mass * g]
        fz3 = [0,-node3.mass * g]

        force01 = phanim.springForce(C, l1, node0.position, node1.position)
        force12 = phanim.springForce(C, l2, node1.position, node2.position)
        force21 = phanim.springForce(C, l2, node2.position, node1.position)
        forcemouse = phanim.springForce(10, 0, screen.mousePos, node2.position)*0

        force23 = phanim.springForce(C, l3, node2.position, node3.position)
        force32 = phanim.springForce(C, l3, node3.position, node2.position)

        force1 = phanim.vadd(force01,fz1,force21)
        force2 = phanim.vadd(force12,fz2,force32)
        force3 = phanim.vadd(force23,fz3)

        node1.eulerODESolver(force1, screen.dt)
        node2.eulerODESolver(force2, screen.dt)
        node3.eulerODESolver(force3, screen.dt)
        

def update_screen(screen):
    screen.draw(grid2,grid1)
    springLines = [
        [node0.position,node1.position,(80,80,80)],
        [node1.position,node2.position,(80,80,80)],
        [node2.position,node3.position,(80,80,80)],
    ]
    screen.drawLines(springLines,10)

    arrow1.setDirection(node1.position,node1.velocity,scale=0.2)
    arrow2.setDirection(node2.position,node2.velocity,scale=0.2)
    arrow3.setDirection(node3.position,node3.velocity,scale=0.2)

    if drawVectors:
        screen.draw(arrow1,arrow2,arrow3)

    trail1.add(node1.position,(255,0,0,255))
    trail2.add(node2.position,(0,255,0,255))
    trail3.add(node3.position,(0,0,255,255))

    if drawTrails:
        screen.draw(trail1,trail2,trail3)

    screen.draw(node0,node1,node2,node3)
    
    kinetic1 = 0.5 * node1.mass * phanim.magnitude(node1.velocity)**2
    kinetic2 = 0.5 * node2.mass * phanim.magnitude(node2.velocity)**2
    kinetic3 = 0.5 * node3.mass * phanim.magnitude(node3.velocity)**2

    potential1 = node1.mass * g * node1.position[1]
    potential2 = node2.mass * g * node2.position[1]
    potential3 = node3.mass * g * node3.position[1]

    energy1 = kinetic1+potential1
    energy2 = kinetic2+potential2
    energy3 = kinetic3+potential3
    energy = energy1+energy2+energy3

    graph1.addDataPoint(energy1)
    graph2.addDataPoint(energy2)
    graph3.addDataPoint(energy3)
    graph4.addDataPoint(energy)

    screen.lastEnergy = energy

    screen.draw(graph1,graph2,graph3,graph4)


screen.addUpdater(update_physics,substeps=substeps)
screen.addUpdater(update_screen)
screen.run()