import phanim as ph

myScreen = ph.Screen([1920*0.7,1080*0.7],zoom=6)

grid1 = ph.Grid(1,1,10,10)
grid2 = ph.Grid(0.2,0.2,35,35,width=2)

node1 = ph.Node(pos=[1,0],vel=[0,1])
node2 = ph.Node(pos=[-1,0],vel=[0,-0.5],mass=2)

velarrow1 = ph.Arrow(lineThickness=0.02,pointSize=0.1)
accarrow1 = ph.Arrow(lineThickness=0.02,pointSize=0.1,color='red')
velarrow2 = ph.Arrow(lineThickness=0.02,pointSize=0.1)
accarrow2 = ph.Arrow(lineThickness=0.02,pointSize=0.1,color='red')

G = 4
r=0

def update_physics(screen):
    if screen.t > 0.3:
        force1 = ph.gravity(node1.position, node2.position, G*node1.mass*node2.mass)
        force2 = -force1
        node1.eulerODESolver(force1,screen.dt)
        node2.eulerODESolver(force2,screen.dt)


def update_screen(screen):
    screen.draw(grid2)
    screen.draw(grid1)

    vectorscale = 0.5
    velarrow1.setDirection(node1.position,node1.velocity,scale=vectorscale)
    accarrow1.setDirection(node1.position,node1.accelaration,scale=vectorscale)
    velarrow2.setDirection(node2.position,node2.velocity,scale=vectorscale)
    accarrow2.setDirection(node2.position,node2.accelaration,scale=vectorscale)

    screen.draw(velarrow1,accarrow1,velarrow2,accarrow2)

    screen.draw(node1)
    screen.draw(node2)


myScreen.addUpdater(update_screen)
myScreen.addUpdater(update_physics,substeps=1000)
myScreen.run()