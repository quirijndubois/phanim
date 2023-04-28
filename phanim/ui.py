import numpy as np
from phanim.functions import *
from copy import deepcopy

class Grid():
    def __init__(self, Xspacing, Yspacing, n_horizontal, n_vertical, color = (100,100,100), width = 1,position = [0,0]):
        self.position = position
        self.lines = []
        self.color = color
        self.lineWidth = width

        self.n_horizontal = n_horizontal
        self.n_vertical = n_vertical
        self.Xspacing = Xspacing
        self.Yspacing = Yspacing

        self.generateGrid()
        
    def generateGrid(self):
        xmax = self.n_horizontal * self.Xspacing
        ymax = self.n_vertical * self.Yspacing
        x_range = np.arange(-self.n_horizontal,self.n_horizontal,self.Xspacing)
        y_range = np.arange(-self.n_vertical,self.n_vertical,self.Yspacing)

        pos = np.array(self.position)
        for x in x_range:
            self.lines.append([[x,ymax]+pos,[x,-ymax]+pos,self.color])
        for y in y_range:
            self.lines.append([[xmax,y]+pos,[-xmax,y]+pos,self.color])

    def createFunction(self,t,old):
        for i in range(len(self.lines)):
            startIndex = 0
            endIndex = 1
            self.lines[i][startIndex] = list((interp2d(self.lines[i][endIndex],old.lines[i][startIndex],t)))  

    def setPosition(self,position):
        self.position = position
        self.reset()
        self.generateGrid()

    def reset(self):
        self.index = 0
        self.lines = []

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
    
    def createFunction(self,t,old):
        self.lineThickness = interp(0,old.lineThickness,t)
        self.pointThickness = interp(0,old.pointThickness,t)

class Axes():
    def __init__(self,position=[0,0],xRange=[-4,4],yRange=[-2,2],lineWidth=1,color=(255,255,255),step=1,numbers=False):
        self.position = position
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
            [[self.xRange[0],0],[self.xRange[1],0],self.color],
            [[0,self.yRange[0]],[0,self.yRange[1]],self.color]
        ]
        xList = np.arange(self.xRange[0],self.xRange[1]+self.step,self.step)
        yList = np.arange(self.yRange[0],self.yRange[1]+self.step,self.step)
        for x in xList:
            if x != 0:
                self.relativeLines.append([[x,0.1],[x,-0.1],self.color])
                if self.showNumbers:
                    self.relativeTexts.append([str(x),[x,-0.2],self.color])
        for y in yList:
            if y != 0:
                self.relativeLines.append([[0.1,y],[-0.1,y],self.color])
                if self.showNumbers:
                    self.relativeTexts.append([str(y),[-0.3,y+0.05],self.color])
        
        self.lines = []
        self.texts = []
        for line in self.relativeLines:
            self.lines.append([vadd(line[0],self.position),vadd(line[1],self.position),line[2]])
        if self.showNumbers:
            for text in self.relativeTexts:
                self.texts.append([text[0],vadd(text[1],self.position),text[2]])
    
    def setPosition(self,position):
        self.position = position
        self.setLines()

    def createFunction(self,t,old):
        for i in range(len(self.lines)):
            startIndex = 1
            endIndex = 0
            self.lines[i][startIndex] = list((interp2d(self.lines[i][endIndex],old.lines[i][startIndex],t)))
        for i in range(len(self.texts)):
            self.texts[i][1] = interp2d([0,0],old.texts[i][1], t)

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
    
    def createFunction(self,t,old):
        self.setEnds(self.start,interp2d(old.start,old.stop,t))

class DottedLine(Line):
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
