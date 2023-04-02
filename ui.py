import numpy as np
from phanim.functions import *

class Grid():
    def __init__(self, Xspacing, Yspacing, n_horizontal, n_vertical, color = (60,60,60), width = 5):
   
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
        self.color = color
        self.lineWidth = lineWidth
        self.index = 0
        self.length = length
        self.segmentLength = segmentLength
    def add(self,position,color):
        self.index += 1
        if self.index%self.segmentLength == 0:
            self.positions.append([position[0],position[1]])
            if len(self.positions) > 1:
                line = [self.positions[-2],self.positions[-1],color]
                self.lines.append(line)
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

class Graph():
    def __init__(self,pos=[0,0],xSize=1,ySize=1,xrange=500,lineWidth = 2,color="red"):
        self.position = pos
        self.data = []
        self.xSize = xSize
        self.ySize = ySize
        self.drawtype = "lines"
        self.color = color
        self.lineWidth = lineWidth
        self.range = xrange
        self.lines = []
    def setLines(self):
        self.points = []
        self.max = max(abs(np.array(self.data)))
        for i in range(len(self.data)):
            if len(self.data) > 0 and self.max > 0:
                self.points.append([
                    i / len(self.data) * self.xSize + self.position[0],
                    self.data[i] / self.max * self.ySize + self.position[1]
                ])
        self.lines = pointsToLines(self.points,self.color)

    def setData(self,data):
        self.data = data
    def addDataPoint(self,dataPoint):
        self.data.append(dataPoint)
        self.setLines()
        if len(self.data) > self.range:
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
        pointstart = self.end - normalize(direction)*self.pointlength

        return [
            self.begin - normal*self.lineThickness/2,
            self.begin + normal*self.lineThickness/2,
            pointstart + normal*self.lineThickness/2,
            pointstart + normal*self.pointThickness/2,
            self.end,
            pointstart - normal*self.pointThickness/2,
            pointstart - normal*self.lineThickness/2
        ]

    def setPosition(self,begin,end):
        self.begin = begin
        self.end = end
        self.polygons = [self.calculateVertices()]

    def setDirection(self,begin,direction,scale=1):
        self.setPosition(begin,begin+np.array(direction)*scale)

        



        
