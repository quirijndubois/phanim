from phanim.functions import *
from copy import copy


class Node():
    def __init__(self, pos=[0, 0], vel=[0, 0], radius=0.2, color=(0, 0, 0), borderColor=(200, 200, 200), borderSize=0.3, mass=1, charge=0, interactivityType="position"):
        self.velocity = np.array(vel, dtype='float64')
        self.accelaration = np.array([0.0, 0.0])
        self.accelarationAVG = np.array([0.0, 0.0])
        self.mass = mass
        self.radius = radius
        self.color = color
        self.borderColor = borderColor
        self.borderSize = borderSize
        self.interactivityType = interactivityType
        self.charge = charge
        self.selected = False
        self.force = np.array([0.0, 0.0])
        self.interactiveForce = np.array([0.0, 0.0])
        self.setPosition(pos)

    def setCircles(self):
        self.circles = [[self.radius, [0, 0], self.borderColor], [
            self.radius*(1-self.borderSize), [0, 0], self.color]]

    def setColor(self, color):
        self.color = color
        self.setCircles()

    def setPosition(self, position):
        self.position = np.array(position, dtype='float64')

    def setRadius(self, radius):
        self.radius = radius
        self.setCircles()

    def eulerODESolver(self, force, dt):

        force = np.array(force)+self.interactiveForce

        self.accelaration = force / self.mass

        AVGlength = 10000
        self.accelarationAVG = interp(
            self.accelarationAVG, self.accelaration, 1/AVGlength)

        self.velocity += self.accelaration * dt

        self.position += self.velocity * dt

    def rkODESolver(self, force, dt):
        pass

    def createFunction(self, t, old):
        size = calculateBezier([0, 0], [0, 3], [0.5, 1.5], [
                               1, 1], t)[1]*old.radius
        self.setRadius(size)

    def updateInteractivity(self, screen):
        self.interactiveForce = [0, 0]
        if self in screen.selectedObjects:
            if not self.selected:
                self.offset = self.position - screen.GlobalCursorPosition

            self.setColor((100, 100, 100))
            if screen.dragging:
                if self.interactivityType == "position":
                    self.setPosition(
                        screen.mousePos+screen.camera.position+self.offset)
                    if self.selected:
                        self.velocity = (self.position-self.lasPos)/screen.dt/2
                    self.selected = True
                    self.lasPos = copy(self.position)
                if self.interactivityType == "force":
                    screen.draw(
                        Line(start=screen.GlobalCursorPosition, stop=self.position))
                    self.interactiveForce = (
                        screen.GlobalCursorPosition-self.position)*300
                    self.velocity = self.velocity*0.80
            else:
                self.selected = False
        else:
            self.setColor((0, 0, 0))


class Value():
    def __init__(self, value=0):
        self.value = value

    def setValue(self, value):
        self.value = value

    def getValue(self):
        return self.value


class Electron(Node):
    def __init__(self, *args, lineWidth=1, signSize=0.05, **kwargs):
        super().__init__(*args, **kwargs)
        self.signSize = signSize
        self.lineWidth = lineWidth
        self.lineColor = self.borderColor
        self.setSign(self.signSize)

    def setSign(self, size):
        if self.charge > 0:
            self.lines = [
                [[0, size], [0, -size], self.lineColor],
                [[size, 0], [-size, 0], self.lineColor]
            ]
        elif self.charge < 0:
            self.lines = [
                [[size, 0], [-size, 0], self.lineColor]
            ]

    def createFunction(self, t, old):
        super().createFunction(t, old)
        self.setSign(t*self.signSize)


class Grid():
    def __init__(self, Xspacing, Yspacing, n_horizontal, n_vertical, color=(100, 100, 100), width=1, position=[0, 0]):
        self.position = np.array(position)
        self.lines = []
        self.color = color
        self.lineWidth = width

        self.n_horizontal = n_horizontal
        self.n_vertical = n_vertical
        self.Xspacing = Xspacing
        self.Yspacing = Yspacing

        self.generateGrid()

    def generateGrid(self):
        self.lines = []
        xmax = self.n_horizontal * self.Xspacing
        ymax = self.n_vertical * self.Yspacing
        x_range = np.arange(-self.n_horizontal,
                            self.n_horizontal, self.Xspacing)
        y_range = np.arange(-self.n_vertical, self.n_vertical, self.Yspacing)

        pos = np.array([0, 0])
        for x in x_range:
            self.lines.append(
                [np.array([x, ymax])+pos, np.array([x, -ymax])+pos, self.color])
        for y in y_range:
            self.lines.append(
                [np.array([xmax, y])+pos, np.array([-xmax, y])+pos, self.color])

    def createFunction(self, t, old):
        for i in range(len(self.lines)):
            startIndex = 0
            endIndex = 1
            self.lines[i][startIndex] = list(
                (interp(self.lines[i][endIndex], old.lines[i][startIndex], t)))

    def setPosition(self, position):
        self.position = position

    def reset(self):
        self.index = 0
        self.lines = []


class Arrow():
    def __init__(self, begin=[0, 0], end=[0, 1], color=(0, 0, 255), lineThickness=0.06, pointSize=0.2):
        self.begin = np.array(begin)
        self.end = np.array(end)
        self.position = [0, 0]
        self.lineThickness = lineThickness
        self.pointThickness = pointSize
        self.pointlength = pointSize
        self.color = color
        self.sizeRatio = 1
        self.polygons = [self.calculateVertices()]

    def setColor(self, color):
        self.color = color

    def calculateVertices(self):
        if self.sizeRatio != 1:
            end = interp(self.begin, self.end, self.sizeRatio)
        else:
            end = self.end

        direction = end - self.begin
        length = magnitude(direction)
        normal = np.array(
            normalize(np.array([-direction[1], direction[0]]), mag=length))
        pointstart = interp(end, self.begin, self.pointlength)

        return [
            self.begin - normal*(self.lineThickness*length)/2,
            self.begin + normal*(self.lineThickness*length)/2,
            pointstart + normal*(self.lineThickness*length)/2,
            pointstart + normal*(self.pointThickness*length)/2,
            end,
            pointstart - normal*(self.pointThickness*length)/2,
            pointstart - normal*(self.lineThickness*length)/2
        ]

    def setPosition(self, begin, end):
        self.begin = begin
        self.end = end
        self.polygons = [self.calculateVertices()]

    def setDirection(self, begin, direction, scale=1):
        self.setPosition(begin, begin+np.array(direction)*scale)

    def createFunction(self, t, old):
        self.sizeRatio = t
        self.polygons = [self.calculateVertices()]


class Axes():
    def __init__(self, position=[0, 0], xRange=[-4, 4], yRange=[-2, 2], lineWidth=1, color=(255, 255, 255), step=1, numbers=False):
        self.position = np.array(position)
        self.xRange = xRange
        self.yRange = yRange
        self.lineWidth = lineWidth
        self.color = color
        self.step = step
        self.showNumbers = numbers
        self.setLines()

    def setLines(self):
        self.relativeTexts = []
        self.relativeLines = [
            [[self.xRange[0], 0], [self.xRange[1], 0], self.color],
            [[0, self.yRange[0]], [0, self.yRange[1]], self.color]
        ]
        xList = np.arange(self.xRange[0], self.xRange[1]+self.step, self.step)
        yList = np.arange(self.yRange[0], self.yRange[1]+self.step, self.step)
        for x in xList:
            if x != 0:
                self.relativeLines.append([[x, 0.1], [x, -0.1], self.color])
                if self.showNumbers:
                    self.relativeTexts.append([str(x), [x, -0.2], self.color])
        for y in yList:
            if y != 0:
                self.relativeLines.append([[0.1, y], [-0.1, y], self.color])
                if self.showNumbers:
                    self.relativeTexts.append(
                        [str(y), [-0.3, y+0.05], self.color])

        self.lines = []
        self.texts = []
        for line in self.relativeLines:
            self.lines.append(
                [line[0]+self.position, line[1]+self.position, line[2]])
        if self.showNumbers:
            for text in self.relativeTexts:
                self.texts.append([text[0], text[1]+self.position, text[2]])

    def setPosition(self, position):
        self.position = position
        self.setLines()

    def createFunction(self, t, old):
        for i in range(len(self.lines)):
            startIndex = 1
            endIndex = 0
            self.lines[i][startIndex] = list(
                (interp(self.lines[i][endIndex], old.lines[i][startIndex], t)))
        for i in range(len(self.texts)):
            self.texts[i][1] = interp([0, 0], old.texts[i][1], t)


class Line():
    def __init__(self, start=[0, 0], stop=[1, 0], color=(255, 255, 255), lineWidth=5, position=[0, 0]):
        self.position = np.array([0, 0])
        self.start = np.array(start)
        self.stop = np.array(stop)
        self.color = color
        self.lineWidth = lineWidth

        self.setLines()

    def setLines(self, ratio=1):
        self.lines = []
        if ratio == 1:
            self.lines.append([self.start, self.stop, self.color])
        else:
            self.lines.append(
                [self.start, interp(self.start, self.stop, ratio), self.color])

    def setEnds(self, start, stop):
        self.start = start
        self.stop = stop
        self.setLines()

    def createFunction(self, t, old):
        self.setLines(ratio=t)


class DottedLine(Line):
    def __init__(self, start=[0, 0], stop=[1, 0], color=(255, 255, 255), lineWidth=5, stripeLength=0.1, position=[0, 0]):
        self.position = np.array([0, 0])
        self.start = np.array(start)
        self.stop = np.array(stop)
        self.color = color
        self.lineWidth = lineWidth
        self.stripeLength = stripeLength
        self.setLines()

    def setLines(self, ratio=1):

        start = self.start
        stop = interp(self.start, self.stop, ratio)

        self.lines = []
        r = ((start[0]-stop[0])**2+(start[1]-stop[1])**2)**(0.5)

        if r != 0:
            res = self.stripeLength/r
        else:
            res = 1

        array = np.arange(0, 1, res)
        for index, t in enumerate(array):
            if index % 2 == 1:
                self.lines.append(
                    [interp(start, stop, t), interp(start, stop, lastt), self.color])
            else:
                if index == len(array)-1:
                    self.lines.append(
                        [interp(start, stop, t), interp(start, stop, 1), self.color])
                lastt = t

    def setEnds(self, start, stop):
        self.start = start
        self.stop = stop
        self.setLines()


class Text():
    def __init__(self, text="Hello World!", color=(255, 255, 255), size=20, position=[0, 0]):
        self.text = str(text)
        self.position = np.array(position, dtype='float64')
        self.color = color
        self.size = size

        self.__setText()

    def setText(self, text):
        self.text = str(text)
        self.__setText()

    def setPosition(self, position):
        self.position = position
        self.__setText()

    def __setText(self, ratio=1):
        self.texts = []

        if ratio == 1:
            self.texts.append([self.text, self.size, self.color])
        else:
            raise NotImplementedError

    def createFunction(self, t, old):
        self.setLines(ratio=t)
