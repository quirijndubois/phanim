from phanim import *

myScreen = Screen()

grid = Grid(1,1,10,10)
arrow =Arrow(color=color.blue)
lines = DottedLine(),DottedLine()

def update(screen):
  arrow.setDirection([0,0],screen.mousePos)
  lines[0].setEnds([screen.mousePos[0],0],screen.mousePos)
  lines[1].setEnds([0,screen.mousePos[1]],screen.mousePos)

myScreen.addUpdater(update)

myScreen.wait(60)
myScreen.play(Create(grid))
myScreen.play(Create(arrow))
myScreen.play(Create(lines[0]),Create(lines[1]))

myScreen.run()