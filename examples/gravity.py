from phanim import *

screen = Screen(fullscreen=True)

grid1 = Grid(1,1,10,10)
grid2 = Grid(0.2,0.2,35,35,width=2)

node1 = Node(pos=[2,0],vel=[0,1.5],mass=1)
node2 = Node(pos=[-2/3,0],vel=[0,-3/4],mass=2)

velarrow1 = Arrow(lineThickness=0.02,pointSize=0.1)
accarrow1 = Arrow(lineThickness=0.02,pointSize=0.1,color='red')
velarrow2 = Arrow(lineThickness=0.02,pointSize=0.1)
accarrow2 = Arrow(lineThickness=0.02,pointSize=0.1,color='red')

G = 6
r=0

def update_physics(screen):
    if screen.t > 0.3:
        force1 = gravity(node1.position, node2.position, G*node1.mass*node2.mass)
        force2 = -force1
        node1.eulerODESolver(force1,screen.dt)
        node2.eulerODESolver(force2,screen.dt)


def update_screen(screen):

    velvectorscale = 0.5
    accvectorscale = 0.3

    velarrow1.setDirection(node1.position,node1.velocity,scale=velvectorscale)
    accarrow1.setDirection(node1.position,node1.accelaration,scale=accvectorscale)
    velarrow2.setDirection(node2.position,node2.velocity,scale=velvectorscale)
    accarrow2.setDirection(node2.position,node2.accelaration,scale=accvectorscale)

    # screen.draw(velarrow1,accarrow1,velarrow2,accarrow2)

screen.play(Create(DGrid()))
screen.play(Create(node1))
screen.play(Create(node2))
screen.play(Create(velarrow1))
screen.play(Create(velarrow2))
screen.play(Create(accarrow1))
screen.play(Create(accarrow2))
screen.addUpdater(update_screen)
screen.addUpdater(update_physics,substeps=1000)
screen.run()