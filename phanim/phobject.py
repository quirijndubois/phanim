import phanim.functions as pf

class Node():
    def __init__(self,pos=[0,0],vel=[0,0],radius = 0.2, color = (0,0,0), borderColor = (200,200,200),borderSize=0.3,mass = 1):
        self.velocity = vel
        self.accelaration = [0,0]
        self.accelarationAVG = [0,0]
        self.mass = mass
        self.radius = radius
        self.color = color
        self.borderColor = borderColor
        self.borderSize = borderSize
        self.setPosition(pos)
    
    def setCircles(self):
        self.circles = [[self.radius,[0,0],self.borderColor],[self.radius*(1-self.borderSize),[0,0],self.color]]
    
    def setColor(self,color):
        self.color = color
        self.setCircles()

    def setPosition(self,position):
        self.position = position
    
    def setRadius(self,radius):
        self.radius = radius
        self.setCircles()

    def eulerODESolver(self,force,dt):

        self.accelaration[0] = force[0] / self.mass
        self.accelaration[1] = force[1] / self.mass

        AVGlength = 10000
        self.accelarationAVG = pf.interp2d(self.accelarationAVG, self.accelaration, 1/AVGlength)

        self.velocity[0] += self.accelaration[0] * dt
        self.velocity[1] += self.accelaration[1] * dt

        self.position[0] += self.velocity[0] * dt
        self.position[1] += self.velocity[1] * dt

    def rkODESolver(self,force,dt):
        pass

    def createFunction(self,t,old):
        size = pf.calculateBezier([0,0],[0,3],[0.5,1.5],[1,1],t)[1]*old.radius
        self.setRadius(size)

class Value():
    def __init__(self,value = 0):
        self.value = value
    
    def setValue(self,value):
        self.value = value

    def getValue(self):
        return self.value

class Electron(Node):
    def __init__(self, pos=[0,0], vel=[0,0], radius=0.2, color=(255,255,255),borderColor=(0,0,0),borderSize = 0.05, mass=1,positive = True):
        super().__init__(pos, vel, radius, color, borderColor,borderSize, mass)
        self.plusSize = 0.08
        self.lineWidth = 3
        self.positive = positive
        self.setSign(self.plusSize)

    def setSign(self,size):
        if self.positive:
            self.lines = [
                [[0,size],[0,-size],(0,0,0)],
                [[size,0],[-size,0],(0,0,0)]
            ]
        else:
            self.lines = [
                [[size,0],[-size,0],(0,0,0)]
            ]      

    def createFunction(self, t, old):
        super().createFunction(t, old)
        self.setSign(t*self.plusSize)