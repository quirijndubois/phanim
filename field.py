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
            direction = np.array(point[1])*self.vectorScale

            if direction[0]**2+direction[1]**2 > 1:
                arrow.setDirection(point[0],phanim.functions.normalize(direction),scale=self.maxVectorScale)
            else:
                arrow.setDirection(point[0],(direction),scale=self.maxVectorScale)

            self.arrows.append(arrow)