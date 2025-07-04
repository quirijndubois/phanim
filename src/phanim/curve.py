from .functions import *
from .color import *
from .base_phobject import *


class Curve(Phobject):
    def __init__(self, strokeWidth=0.05, points=[], **kwargs):
        super().__init__(**kwargs)
        self.strokeWidth = strokeWidth
        self.points = points
        self.setShapes()

    def setShapes(self):
        self.setPoints(self.points)

    def setPoints(self, points):
        self.points = np.array(points)
        self.__setNormals()
        self.__setPolygons()

    def __setNormals(self):
        self.pointsWithNormals = []
        if len(self.points) > 1:
            n = self.points[0] - self.points[1]
            n = [-n[1], n[0]]
            self.pointsWithNormals.append([self.points[0], n])
            for i in range(1, len(self.points)-1):
                n1 = self.points[i-1] - self.points[i]
                n1 = np.array([-n1[1], n1[0]])
                n2 = self.points[i] - self.points[i+1]
                n2 = np.array([-n2[1], n2[0]])
                normal = (n1+n2)/2
                self.pointsWithNormals.append([self.points[i], normal])
            n = self.points[-2] - self.points[-1]
            n = [-n[1], n[0]]
            self.pointsWithNormals.append([self.points[-1], n])

    def __setPolygons(self):
        self.polygons = []
        for i in range(len(self.pointsWithNormals)-1):
            self.polygons.append([
                self.pointsWithNormals[i][0] +
                normalize(self.pointsWithNormals[i][1])*self.strokeWidth/2,
                self.pointsWithNormals[i][0] -
                normalize(self.pointsWithNormals[i][1])*self.strokeWidth/2,
                self.pointsWithNormals[i+1][0] - normalize(
                    self.pointsWithNormals[i+1][1])*self.strokeWidth/2,
                self.pointsWithNormals[i+1][0] +
                normalize(self.pointsWithNormals[i+1][1])*self.strokeWidth/2
            ])
        self.polygons = np.array(self.polygons)

    def createFunction(self, t, old):
        res = len(old.points)
        self.setPoints(old.points[:int(t*res)])

    def transformFunction(self, t, old, new):
        newpoints = []

        r_old, g_old, b_old = old.color
        r_new, g_new, b_new = new.color

        self.color = (
            interp(r_old, r_new, t),
            interp(g_old, g_new, t),
            interp(b_old, b_new, t)
        )

        self.setPosition(interp(old.position, new.position, t))

        for i in range(len(old.points)):
            newpoints.append(interp(old.points[i], new.points[i], t))
        self.setPoints(newpoints)


class BezierCurve(Curve):
    def __init__(self, corners=[[1, 1], [-1, 1], [-1, -1], [1, -1]], resolution=100, **kwargs):
        super().__init__(**kwargs)
        self.corners = np.array(corners)
        self.resolution = resolution
        self.__setBezier()

    def __setBezier(self):
        points = []
        for t in np.linspace(0, 1, self.resolution):
            points.append(calculateBezier(
                self.corners[0], self.corners[1], self.corners[2], self.corners[3], t))
        self.setPoints(points)

    def setHandles(self, points):
        self.corners = points
        self.__setBezier()


class PlotGraph(Curve):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # TODO make this easier with arrays!
    def setData(self, x, y):
        points = []
        if len(x) == len(y):
            for i in range(len(x)):
                points.append([x[i], y[i]])
        self.setPoints(points)


class LiveGraph():
    def __init__(self, pos=[0, 0], xSize=[-1, 1], ySize=[-1, 1], yRange=[0, 0], liveRange=500, lineWidth=2, color=red, numbers=False):
        self.position = np.array(pos)
        self.data = []
        self.xSize = np.array(xSize)
        self.ySize = np.array(ySize)
        self.yRange = np.array(yRange)
        self.color = color
        self.lineWidth = lineWidth
        self.liveRange = liveRange
        self.lines = []
        self.texts = [[], []]
        self.numbers = numbers

    def setLines(self):
        self.points = []
        if self.yRange[1] == 0 and self.yRange[0] == 0:
            self.max = max(np.array(self.data))
            self.min = min(np.array(self.data))
        else:
            self.min = self.yRange[0]
            self.max = self.yRange[1]

        for i in range(len(self.data)):
            if len(self.data) > 0 and self.max > 0:
                self.points.append([
                    interp(self.xSize[0], self.xSize[1], i /
                           len(self.data))+self.position[0],
                    mapRange(self.data[i], self.min, self.max,
                             self.ySize[0], self.ySize[1])+self.position[1]
                ])
        self.lines = pointsToLines(self.points, self.color)

    def setTexts(self):
        text = str(round(self.max, 1))
        pos = [
            self.position[0] + self.xSize[0],
            self.position[1] + self.ySize[1]
        ]
        self.texts[0] = [text, pos, self.color]

        text = str(round(self.min, 1))
        pos = [
            self.position[0] + self.xSize[0],
            self.position[1] + self.ySize[0]
        ]
        self.texts[1] = [text, pos, self.color]

    def setData(self, data):
        self.data = data
        self.setLines()
        self.setTexts()

    def addDataPoint(self, dataPoint):
        self.data.append(dataPoint)
        self.setLines()
        if self.numbers:
            self.setTexts()
        if len(self.data) > self.liveRange:
            self.data.pop(0)


class FPScounter(LiveGraph):
    def __init__(self, pos=[-3.5, 2], xSize=[-1, 1], ySize=[-1, 1], yRange=[0, 100], liveRange=360, lineWidth=2, color=(255, 255, 255), numbers=False):
        super().__init__(pos, xSize, ySize, yRange, liveRange, lineWidth, color, numbers)

    def update(self, screen):
        if screen.dt != 0:
            self.addDataPoint(1/screen.dt)


class Trail(Phobject):
    def __init__(self, color=(255, 255, 255), lineWidth=3, length=150, segmentLength=1, opacity=1):
        self.opacity = opacity
        self.positions = []
        self.position = np.array([0, 0])
        self.lines = []
        self.index = 0
        self.color = color
        self.lineWidth = lineWidth
        self.length = length
        self.segmentLength = segmentLength
        self.setRotation(0)

    def add(self, position, color, connected=True):
        self.index += 1
        if self.index % self.segmentLength == 0:
            self.positions.append([position[0], position[1]])
            if len(self.positions) > 1:
                line = [self.positions[-2], self.positions[-1], color]
                if connected:
                    self.lines.append(line)
                else:
                    self.lines.append([line[1], line[1], color])
            if len(self.positions) > self.length/self.segmentLength:
                self.positions.pop(0)
                self.lines.pop(0)
        self.__setLines()

    def __setLines(self):
        for i in range(len(self.lines)):
            alpha = int(i/self.length*254)*self.opacity
            self.lines[i][2] = (
                self.lines[i][2][0],
                self.lines[i][2][1],
                self.lines[i][2][2],
                alpha
            )

    def createFunction(self, t, old):
        self.opacity = interp(0, 1, t)
        self.__setLines()
