import phanim as p

grid1 = p.Grid(1,1,10,10,width=1)
grid2 = p.Grid(0.5,0.5,20,20,width=1,color=(30,30,30))

screen = p.Screen([1000,600],background=(10,15,20),zoom=15)

pos = [[0,1],[2,1],[4,1]]
nodes = p.Node(pos=pos[0]),p.Node(pos=pos[1]),p.Node(pos=pos[2])
nodes[1].velocity = [0,3]
nodes[2].velocity = [0,6]

trail = p.Trail(length=150,lineWidth=3)

C = 10**6
l = 2
G = 10

def update_physics(screen):
    fz = [0,-G]
    spring01 = p.springForce(C,l,nodes[0].position,nodes[1].position)
    spring12 = p.springForce(C,l,nodes[1].position,nodes[2].position)
    spring21 = p.springForce(C,l,nodes[2].position,nodes[1].position)

    nodes[1].eulerODESolver(spring01+spring21+fz, screen.dt)
    nodes[2].eulerODESolver(spring12+fz, screen.dt)

def update(screen):
    screen.draw(grid2,grid1)

    springLines = [
        [nodes[0].position,nodes[1].position,(100,100,100)],
        [nodes[1].position,nodes[2].position,(100,100,100)]
    ]
    screen.drawLines(springLines,10)

    trail.add(nodes[2].position,(255,150,100))
    screen.draw(trail)

    screen.draw(*nodes)

screen.addUpdater(update_physics,substeps=100)
screen.addUpdater(update)
screen.run()

