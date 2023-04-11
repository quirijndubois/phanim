import phanim as p


screen = p.Screen((1600,900),fontSize=0.7)

grids = p.Grid(0.5, 0.5, 20, 20,color=(30,30,30)),p.Grid(1, 1, 10, 10)
curve = p.BezierCurve(res=100,color=(150,150,255))
lines = p.Line(lineWidth=2),p.Line(lineWidth=2),p.dottedLine(lineWidth=2)
title = p.Text(text="Bezier curve",pos=[-1.6,2.7])

nodes = []

def update(screen):
    screen.draw(*grids)

    if len(nodes) == 4:
        screen.closest = p.findClosest([nodes[0].position,nodes[1].position,nodes[2].position,nodes[3].position],screen.mousePos)
        if p.distSq(nodes[screen.closest].position,screen.mousePos) > 1:
            screen.closest = -1

        curve.setPoint([nodes[0].position,nodes[1].position,nodes[2].position,nodes[3].position])
        lines[0].setEnds(nodes[0].position, nodes[1].position)
        lines[1].setEnds(nodes[2].position, nodes[3].position)
        lines[2].setEnds(nodes[1].position, nodes[2].position)
        screen.draw(*lines)
        screen.draw(curve)

    screen.draw(title)
    screen.draw(*nodes)

def click(screen):
    if len(nodes) < 4:
        nodes.append(p.Node(pos=screen.mousePos,radius = 0.1))

def drag(screen):
    if len(nodes) == 4 and screen.closest != -1:
        nodes[screen.closest].setPosition(screen.mousePos)

screen.addUpdater(update)
screen.addMouseClickUpdater(click)
screen.addMouseDragUpdater(drag)
screen.run()
