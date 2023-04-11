import numpy as np
from phanim.functions import *

class Grid():
    def __init__(self, Xspacing, Yspacing, n_horizontal, n_vertical, color = (60,60,60), width = 1):
   
        self.lines = []
        self.color = color
        self.lineWidth = width

        xmax = n_horizontal * Xspacing
        ymax = n_vertical * Yspacing

        x_range = np.arange(-n_horizontal,n_horizontal,Xspacing)
        y_range = np.arange(-n_vertical,n_vertical,Yspacing)

        for x in x_range:
            self.lines.append([[x,ymax],[x,-ymax],self.color])
        for y in y_range:
            self.lines.append([[xmax,y],[-xmax,y],self.color])
    
class Trail():
    def __init__(self,color="white",lineWidth = 1,length=50,segmentLength=1):
        self.positions = []
        self.lines = []
        self.index = 0
        self.color = color
        self.lineWidth = lineWidth
        self.length = length
        self.segmentLength = segmentLength
    def add(self,position,color):
        self.index += 1
        if self.index%self.segmentLength == 0:
            self.positions.append([position[0],position[1]])
            if len(self.positions) > 1:
                line = [self.positions[-2],self.positions[-1],color]
                if abs(line[0][0] - line[1][0]) < 0.5 and abs(line[0][1] - line[1][1]) < 0.5:
                    self.lines.append(line)
                else:
                    self.lines.append([line[1],line[1],color])
            if len(self.positions) > self.length/self.segmentLength:
                self.positions.pop(0)
                self.lines.pop(0)
        for i in range(len(self.lines)):
            alpha = int(i/self.length*254)
            self.lines[i][2] = (
                self.lines[i][2][0],
                self.lines[i][2][1],
                self.lines[i][2][2],
                alpha
            )
    def reset(self):
        self.index = 0
        self.position = []
        self.lines = []

class Graph():
    def __init__(self,pos=[0,0],xSize=[-1,1],ySize=[-1,1],yRange=[0,0],liveRange=500,lineWidth = 2,color="red"):
        self.position = pos
        self.data = []
        self.xSize = xSize
        self.ySize = ySize
        self.yRange = yRange
        self.color = color
        self.lineWidth = lineWidth
        self.liveRange = liveRange
        self.lines = []
        self.texts = [[],[]]
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
                    interp(self.xSize[0],self.xSize[1],i / len(self.data))+self.position[0],
                    mapRange(self.data[i], self.min, self.max, self.ySize[0], self.ySize[1])+self.position[1]
                ])
        self.lines = pointsToLines(self.points,self.color)

    def setTexts(self):
        text = str(round(self.max,1))
        pos = [
            self.position[0] + self.xSize[0],
            self.position[1] + self.ySize[1]
        ]
        self.texts[0] = [text,pos,self.color]

        text = str(round(self.min,1))
        pos = [
            self.position[0] + self.xSize[0],
            self.position[1] + self.ySize[0]
        ]
        self.texts[1] = [text,pos,self.color]

    def setData(self,data):
        self.data = data
        self.setLines()
        self.setTexts()

    def addDataPoint(self,dataPoint):
        self.data.append(dataPoint)
        self.setLines()
        self.setTexts()
        if len(self.data) > self.liveRange:
            self.data.pop(0)

class Arrow():
    def __init__(self,begin=[0,0],end=[0,1],color="blue",lineThickness=0.06,pointSize=0.2):
        self.begin = begin
        self.end = end
        self.lineThickness = lineThickness
        self.pointThickness = pointSize
        self.pointlength = pointSize
        self.color = color
        self.polygons = [self.calculateVertices()]

    def calculateVertices(self):
        direction = np.array([self.end[0] - self.begin[0],self.end[1] - self.begin[1]])
        normal = normalize([-direction[1],direction[0]])
        length = magnitude(direction)
        # pointstart = self.end - normalize(direction)*self.pointlength
        pointstart = interp2d(self.end, self.begin,self.pointlength)

        return [
            self.begin - normal*(self.lineThickness*length)/2,
            self.begin + normal*(self.lineThickness*length)/2,
            pointstart + normal*(self.lineThickness*length)/2,
            pointstart + normal*(self.pointThickness*length)/2,
            self.end,
            pointstart - normal*(self.pointThickness*length)/2,
            pointstart - normal*(self.lineThickness*length)/2
        ]

    def setPosition(self,begin,end):
        self.begin = begin
        self.end = end
        self.polygons = [self.calculateVertices()]

    def setDirection(self,begin,direction,scale=1):
        self.setPosition(begin,begin+np.array(direction)*scale)

        
class BezierCurve():
    def __init__(self,color = "white",res = 100,lineWidth = 0.05):
        self.points = [[0,0],[1,2],[2,-1],[3,0]]
        self.color = color
        self.res = res
        self.lineWidth = lineWidth
        self.setCurvePoints()
        self.setPolygons()
    
    def setCurvePoints(self):
        self.curvePoints = []
        a = np.array(self.points[0])
        b = np.array(self.points[1])
        c = np.array(self.points[2])
        d = np.array(self.points[3])
        for t in np.linspace(0,1,self.res):
            end = (
                a*(-t**3+3*t**2-3*t+1)+
                b*(3*t**3-6*t**2+3*t)+
                c*(-3*t**3+3*t**2)+
                d*(t**3)
            )
            derivative = (
                a*(-3*t**2+6*t-3)+
                b*(9*t**2-12*t+3)+
                c*(-9*t**2+6*t)+
                d*(3*t**2)
            )
            normal = [-derivative[1],derivative[0]]
            self.curvePoints.append([end,normal,derivative])

    def setPolygons(self):
        self.polygons = []
        for i in range(len(self.curvePoints)-1):
            self.polygons.append([
                self.curvePoints[i][0] + normalize(self.curvePoints[i][1])*self.lineWidth/2,
                self.curvePoints[i][0] - normalize(self.curvePoints[i][1])*self.lineWidth/2,
                self.curvePoints[i+1][0] - normalize(self.curvePoints[i+1][1])*self.lineWidth/2,
                self.curvePoints[i+1][0] + normalize(self.curvePoints[i+1][1])*self.lineWidth/2
            ])

    def setPoint(self,points):
        self.points = points
        self.setCurvePoints()
        self.setPolygons()

class Line():
    def __init__(self,start=[0,0],stop=[1,0],color = "white",lineWidth = 5):
        self.start = start
        self.stop = stop
        self.color = color
        self.lineWidth = lineWidth

        self.setLines()

    def setLines(self):
        self.lines = []
        self.lines.append([self.start,self.stop,self.color])

    def setEnds(self,start,stop):
        self.start = start
        self.stop = stop
        self.setLines()

class dottedLine():
    def __init__(self,start=[0,0],stop=[1,0],color = "white",lineWidth = 5,stripeLength = 0.1):
        self.start = start
        self.stop = stop
        self.color = color
        self.lineWidth = lineWidth
        self.stripeLength = stripeLength
        self.setLines()

    def setLines(self):
        self.lines = []
        r = ((self.start[0]-self.stop[0])**2+(self.start[1]-self.stop[1])**2)**(0.5)
        index = 0
        for t in np.arange(0,1,self.stripeLength/r):
            if index%2 == 1:
                self.lines.append([interp2d(self.start,self.stop,t),interp2d(self.start,self.stop,lastt),self.color])
            else:
                lastt = t
            index+=1
            

    def setEnds(self,start,stop):
        self.start = start
        self.stop = stop
        self.setLines()
    
class Text():
    def __init__(self,text = "Hello World!", color = "white" , pos = [0,0]):
        self.text = text
        self.color = color
        self.position = pos
        self.texts = [[self.text,self.position,self.color]]
