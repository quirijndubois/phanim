from phanim.functions import *
from copy import copy


class Phobject():
    def __init__(self, position=[0, 0], velocity=[0, 0], color=(255, 255, 255), mass=1, charge=0, static=False):
        self.accelaration = np.array([0.0, 0.0], dtype='float64')
        self.color = color
        self.static = static
        self.selected = False

        self.mass = mass
        self.charge = charge

        self.force = np.array([0.0, 0.0], dtype='float64')
        self.accelaration = np.array([0.0, 0.0], dtype='float64')
        self.accelarationAVG = np.array([0.0, 0.0], dtype='float64')

        self.lines = []
        self.lineWidth = 0
        self.circles = []
        self.polygons = []
        self.texts = []

        self.setPosition(position)
        self.setVelocity(velocity)

    def setPosition(self, position):
        self.position = np.array(position, dtype='float64')

    def setColor(self, color):
        self.color = color
        self.setShapes()

    def setShapes(self):
        pass

    def setVelocity(self, velocity):
        self.velocity = np.array(velocity, dtype='float64')

    def eulerODESolver(self, force, dt):
        force = np.array(force)+self.interactiveForce
        self.accelaration = force / self.mass
        AVGlength = 10000
        self.accelarationAVG = interp(
            self.accelarationAVG, self.accelaration, 1/AVGlength)
        self.velocity += self.accelaration * dt
        self.position += self.velocity * dt

    def createFunction(self, t, old):
        pass

class Node(Phobject):
    def __init__(self, pos=[0, 0], vel=[0, 0], radius=0.2, color=(0, 0, 0), borderColor=(200, 200, 200), borderSize=0.3, mass=1, charge=0, interactivityType="position", static=False):
        super().__init__(pos, vel, color, mass, charge, static)
        self.radius = radius
        self.borderColor = borderColor
        self.borderSize = borderSize
        self.interactivityType = interactivityType
        self.interactiveForce = np.array([0.0, 0.0])
        self.setShapes()

    def setShapes(self):
        self.circles = [[self.radius, [0, 0], self.borderColor], [
            self.radius*(1-self.borderSize), [0, 0], self.color]]

    def setRadius(self, radius):
        self.radius = radius
        self.setShapes()

    def createFunction(self, t, old):
        size = calculateBezier([0, 0], [0, 3], [0.5, 1.5], [
                               1, 1], t)[1]*old.radius
        self.setRadius(size)

    def updateInteractivity(self, screen):
        if self.static:
            GlobalCursorPosition = screen.StaticCursorPosition
            LocalCursorPosition = screen.StaticCursorPosition
            cam = screen.static_camera
        else:
            GlobalCursorPosition = screen.GlobalCursorPosition
            LocalCursorPosition = screen.LocalCursorPosition
            cam = screen.camera

        self.interactiveForce = [0, 0]
        if self in screen.selectedObjects:
            if not self.selected:
                self.offset = self.position - GlobalCursorPosition

            self.setColor((100, 100, 100))
            if screen.dragging:
                if self.interactivityType == "position":
                    self.setPosition(
                        LocalCursorPosition+cam.position+self.offset)
                    if self.selected:
                        self.velocity = (self.position-self.lasPos)/screen.dt/2
                    self.selected = True
                    self.lasPos = copy(self.position)
                if self.interactivityType == "force":
                    screen.draw(
                        Line(begin=GlobalCursorPosition, end=self.position))
                    self.interactiveForce = (
                        GlobalCursorPosition-self.position)*300
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


class Grid(Phobject):
    def __init__(self, Xspacing, Yspacing, n_horizontal, n_vertical, color=(100, 100, 100), width=1, position=[0, 0]):
        super().__init__(position=position, color=color)

        self.lineWidth = width
        self.n_horizontal = n_horizontal
        self.n_vertical = n_vertical
        self.Xspacing = Xspacing
        self.Yspacing = Yspacing

        self.setShapes()

    def setShapes(self):
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


class Line(Phobject):
    def __init__(self, begin=[0, 0], end=[1, 0], color=(255, 255, 255), lineWidth=5, position=[0, 0]):
        super().__init__(position=position, color=color)
        self.begin = np.array(begin)
        self.end = np.array(end)
        self.lineWidth = lineWidth
        self.setShapes()

    def setShapes(self, ratio=1):
        self.lines = []
        if ratio == 1:
            self.lines.append([self.begin, self.end, self.color])
        else:
            self.lines.append(
                [self.begin, interp(self.begin, self.end, ratio), self.color])

    def setEnds(self, begin, end):
        self.begin = np.array(begin)
        self.end = np.array(end)
        self.setShapes()

    def setDirection(self, begin, direction, scale=1):
        self.setEnds(begin, begin+np.array(direction)*scale)

    def createFunction(self, t, old):
        self.setShapes(ratio=t)


class Polygon(Phobject):
    def __init__(self, points, **kwargs):
        super().__init__(**kwargs)
        self.points = points
        self.setShapes()

    def setShapes(self):
        self.polygons = [self.points]



class Arrow(Line):
    def __init__(self, lineThickness=0.06, pointSize=0.2, **kwargs):
        self.lineThickness = lineThickness
        self.pointThickness = pointSize
        self.pointlength = pointSize
        self.sizeRatio = 1
        super().__init__(**kwargs)

    def setShapes(self, ratio=1):
        self.polygons = [self.calculateVertices(ratio)]

    def calculateVertices(self, ratio):
        if ratio != 1:
            end = interp(self.begin, self.end, ratio)
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


class Axes(Phobject):
    def __init__(self, xRange=[-4, 4], yRange=[-2, 2], lineWidth=1, step=1, showNumbers=False, **kwargs):
        super().__init__(**kwargs)
        self.xRange = xRange
        self.yRange = yRange
        self.lineWidth = lineWidth
        self.step = step
        self.showNumbers = showNumbers
        self.setShapes()

    def setShapes(self):
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

    def createFunction(self, t, old):
        for i in range(len(self.lines)):
            startIndex = 1
            endIndex = 0
            self.lines[i][startIndex] = list(
                (interp(self.lines[i][endIndex], old.lines[i][startIndex], t)))
        for i in range(len(self.texts)):
            self.texts[i][1] = interp([0, 0], old.texts[i][1], t)


class DottedLine(Line):
    def __init__(self, stripeLength=0.1, **kwargs):
        self.stripeLength = stripeLength
        super().__init__(**kwargs)

    def setShapes(self, ratio=1):

        start = self.begin
        stop = interp(self.begin, self.end, ratio)

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


class Text(Phobject):
    def __init__(self, text="Hello World!", size=20, **kwargs):
        super().__init__(**kwargs)
        self.text = str(text)
        self.size = size

        self.setShapes()

    def setText(self, text):
        self.text = str(text)
        self.setShapes()

    def setShapes(self, ratio=1):
        self.texts = []

        if ratio == 1:
            self.texts.append([self.text, self.size, self.color])
        else:
            raise NotImplementedError

    def createFunction(self, t, old):
        pass
