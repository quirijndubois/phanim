import numpy as np
import phanim

class Field():
    def __init__(self,resolution=1,size=[5,3],vectorScale=50,maxVectorScale = 0.6,pointSize = 0.2,lineThickness=0.06):
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
        self.charges = charges
        self.lineWidth = lineWidth
        self.color = color
        self.radius = 0.1
        self.linesPerCharge = linesPerCharge
        self.position = [0,0]
        self.generateLines()

    def update(self,charges):
        self.charges = charges
        self.generateLines()

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
                        if category == 1:
                            diff = -diff
                        magsq = phanim.magSquared(diff)
                        if magsq < particleLimit:
                            dobreak = True
                        force = q[1]/magsq*diff
                        totalForce = phanim.vadd(force,totalForce)
                    if dobreak:
                        break
                    positions.append(phanim.vadd(positions[-1],phanim.normalize(totalForce)/8))

                decimateAmount = 20
                if len(positions) > decimateAmount:
                    positions = phanim.decimate(positions,decimateAmount)
                lines = phanim.pointsToLines(positions,self.color)
                for line in lines:
                    self.lines.append(line)