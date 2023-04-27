from .functions import *
import math

class Curve():
    def __init__(self,position=[0,0],strokeWidth=0.05,color=(255,255,255)):
        self.position = position
        self.strokeWidth = strokeWidth
        self.color = color
    
    def setPoints(self,points):
        self.points = points
        self.setNormals()
        self.setPolygons()
    
    def setPosition(self,position):
        self.position = position
        self.setNormals()
        self.setPolygons()

    def setNormals(self):
        self.pointsWithNormals = []
        if len(self.points) > 1:
            n = diff(self.points[0], self.points[1])
            n = [-n[1],n[0]]
            self.pointsWithNormals.append([self.points[0],n])
            for i in range(1,len(self.points)-1):
                n1 = diff(self.points[i-1], self.points[i])
                n1 = np.array([-n1[1],n1[0]])
                n2 = diff(self.points[i], self.points[i+1])
                n2 = np.array([-n2[1],n2[0]])
                normal = (n1+n2)/2
                self.pointsWithNormals.append([self.points[i],normal])
            n = diff(self.points[-2], self.points[-1])
            n = [-n[1],n[0]]
            self.pointsWithNormals.append([self.points[-1],n])

    def setPolygons(self):
        self.polygons = []
        for i in range(len(self.pointsWithNormals)-1):
            self.polygons.append([
                self.pointsWithNormals[i][0] + normalize(self.pointsWithNormals[i][1])*self.strokeWidth/2 + self.position,
                self.pointsWithNormals[i][0] - normalize(self.pointsWithNormals[i][1])*self.strokeWidth/2 + self.position,
                self.pointsWithNormals[i+1][0] - normalize(self.pointsWithNormals[i+1][1])*self.strokeWidth/2 + self.position,
                self.pointsWithNormals[i+1][0] + normalize(self.pointsWithNormals[i+1][1])*self.strokeWidth/2 + self.position
            ])
        
    def createFunction(self,t,old):
        res = len(old.points)
        self.setPoints(old.points[:int(t*res)])

    def transformFunction(self,t,old,new):
        newpoints = []

        r_old,g_old,b_old = old.color
        r_new,g_new,b_new = new.color

        self.color = (
            interp(r_old, r_new, t),
            interp(g_old, g_new, t),
            interp(b_old, b_new, t)
        )

        self.setPosition(interp2d(old.position,new.position,t))

        for i in range(len(old.points)):
            newpoints.append(interp2d(old.points[i],new.points[i],t))
        self.setPoints(newpoints)

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

class Graph(Curve):
    def __init__(self, position=[0,0], width=0.05,color=(255,255,255)):
        super().__init__(position,width,color)
    
    def setData(self,x,y):
        points = []
        if len(x) == len(y):
            for i in range(len(x)):
                points.append([x[i],y[i]])
        self.setPoints(points)

class LiveGraph():
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

