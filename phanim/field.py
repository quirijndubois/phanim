from .group import *
import numpy as np
import phanim
from copy import copy

class Field(Group):
    def __init__(self,fieldFunction = None,spacing = 1, size = [5,5],position=[0,0]):
        super().__init__()

        if fieldFunction == None:
            self.fieldFunction = lambda x,y: normalize([x,y])*spacing*0.5
        else: 
            self.fieldFunction = fieldFunction
        
        self.position = position
        self.spacing = spacing
        self.size = size
        self.setField(self.fieldFunction)

    def setField(self,fieldFunction):
        self.field = []
        for y in range(self.size[1]):
            fieldRow = []
            for x in range(self.size[0]):
                pos = [-(self.size[0]-1)*self.spacing/2+self.spacing*x,-(self.size[1]-1)*self.spacing/2+self.spacing*y]
                fieldRow.append([pos,fieldFunction(pos[0],pos[1])])
            self.field.append(fieldRow)
        self.setArrows()

    def setArrows(self):
        self.groupObjects = []
        for row in self.field:
            for position in row:

                magSQ = magSquared(position[1])
                coloringMagSq = magSQ/50
                if coloringMagSq < 1 and coloringMagSq > 0:
                    color = (
                        phanim.interp(0, 255,coloringMagSq**(1/4)),
                        phanim.interp(55, 0,coloringMagSq),
                        phanim.interp(200, 0,coloringMagSq)
                    )
                else:
                    color = (255,0,0)
                
                if magSQ>self.spacing**2:
                    direction = normalize(position[1])*self.spacing
                else:
                    direction = position[1]

                self.groupObjects.append(Arrow(begin=position[0],end=vadd(position[0],direction),color=color))

    def updateField(self):
        self.setArrows()
                
        

class OldField():
    def __init__(self,resolution=1,size=[5,4],vectorScale=50,maxVectorScale = 0.6,pointSize = 0.2,lineThickness=0.06):
        self.position = [0,0]
        self.vectorScale = vectorScale/resolution
        self.maxVectorScale = maxVectorScale/resolution
        self.pointSize = pointSize/resolution
        self.lineThickness = lineThickness/resolution
        self.size = size
        self.resolution = resolution
        self.sizeRatio = 1
    def setField(self,lambdaFunction):
        x_range = np.arange(-self.size[0], self.size[0],1/self.resolution)
        y_range = np.arange(-self.size[1], self.size[1],1/self.resolution)
        self.field = []
        self.lambdaFunction = lambdaFunction
        for x in x_range:
            for y in y_range:
                self.field.append([[x,y],lambdaFunction(x,y)])

    def generateArrows(self):
        self.arrows = []
        for point in self.field:
            mag = phanim.magnitude(point[1])
            if mag < 1 and mag > 0:
                color = (
                    phanim.interp(0, 255,mag**0.5),
                    phanim.interp(55, 0,mag),
                    phanim.interp(200, 0,mag**2)
                )
            else:
                color = "red"

            arrow = phanim.Arrow(pointSize=0.4,lineThickness=0.1,color=color)
            direction = np.array(point[1])*self.vectorScale*self.sizeRatio

            if direction[0]**2+direction[1]**2 > 1:
                arrow.setDirection(point[0],phanim.functions.normalize(direction),scale=self.maxVectorScale)
            else:
                arrow.setDirection(point[0],(direction),scale=self.maxVectorScale)

            self.arrows.append(arrow)
            self.groupObjects = self.arrows

    def createFunction(self,t,old):
        self.sizeRatio = t
        self.generateArrows()

class ElectricLineField():
    def __init__(self,charges,lineWidth=4,linesPerCharge=20,color=(100,100,100)):
        self.charges = copy(charges)
        self.lineWidth = lineWidth
        self.color = color
        self.radius = 0.1
        self.linesPerCharge = linesPerCharge
        self.position = [0,0]
        self.generateLines()

    def update(self,charges):
        self.charges = copy(charges)
        self.generateLines()

    def fieldFunction(self,x,y):
        position = [x,y]
        totalForce = [0,0]
        for q in self.charges:
            diff = phanim.diff(position,q[0])
            magsq = phanim.magSquared(diff)
            force = q[1]/magsq*diff
            totalForce = phanim.vadd(force,totalForce)
        return totalForce

    def generateLines(self):
        startPositionsPositive = []
        startPositionsNegative = []
        for q in self.charges:
            if q[1] > 0:
                for i in range(self.linesPerCharge):
                    startPositionsPositive.append([
                        q[0][0] + np.cos(i/self.linesPerCharge*2*np.pi)/10,
                        q[0][1] + np.sin(i/self.linesPerCharge*2*np.pi)/10
                    ])
            if q[1] < 0:
                for i in range(self.linesPerCharge):
                    startPositionsNegative.append([
                        q[0][0] + np.cos(i/self.linesPerCharge*2*np.pi)*self.radius,
                        q[0][1] + np.sin(i/self.linesPerCharge*2*np.pi)*self.radius
                    ])
        startPositions = [startPositionsPositive,startPositionsNegative]

        self.lines = []
        particleLimit = (self.radius*0.9)**2
        for category in range(1):
            for startPosition in startPositions[category]:
                positions = [startPosition]
                for i in range(10000):
                    totalForce = [0,0]
                    dobreak = False
                    for q in self.charges:
                        diff = phanim.diff(positions[-1],q[0])
                        magsq = phanim.magSquared(diff)
                        if magsq < particleLimit:
                            dobreak = True
                    if dobreak:
                        break
                    totalForce = self.fieldFunction(positions[-1][0],positions[-1][1])
                    if category == 1:
                        totalForce = -totalForce
                    positions.append(phanim.vadd(positions[-1],phanim.normalize(totalForce)/8))

                decimateAmount = 20
                if len(positions) > decimateAmount:
                    positions = phanim.decimate(positions,decimateAmount)
                lines = phanim.pointsToLines(positions,self.color)
                for line in lines:
                    self.lines.append(line)