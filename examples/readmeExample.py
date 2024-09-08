from phanim import *

myScreen = Screen(grid=False)

grid = Grid(1, 1, 10, 10)
arrow = Arrow(color=color.blue)
lines = DottedLine(), DottedLine()


def update(screen):
    arrow.setDirection([0, 0], screen.GlobalCursorPosition)
    lines[0].setEnds([screen.GlobalCursorPosition[0], 0],
                     screen.GlobalCursorPosition)
    lines[1].setEnds([0, screen.GlobalCursorPosition[1]],
                     screen.GlobalCursorPosition)


myScreen.addUpdater(update)

myScreen.wait(60)
myScreen.play(Create(grid))
myScreen.play(Create(arrow))
myScreen.play(Create(lines[0]), Create(lines[1]))

myScreen.run()
