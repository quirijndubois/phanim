import phanim.functions as pf

class Node():
    def __init__(self,pos=[0,0],vel=[0,0],radius = 0.2, color = (200,200,200),mass = 1):
        self.velocity = vel
        self.accelaration = [0,0]
        self.accelarationAVG = [0,0]
        self.mass = mass
        self.radius = radius
        self.color = color
        self.setPosition(pos)
    
    def setCircles(self):
        self.circles = [[self.radius,self.position,self.color],[self.radius*0.7,self.position,"black"]]
    
    def setColor(self,color):
        self.color = color
        self.setCircles()

    def setPosition(self,position):
        self.position = position
        self.setCircles()
    
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

