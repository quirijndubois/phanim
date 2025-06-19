from phanim.functions import *
from copy import copy


class Phobject():
    def __init__(self, position=[0, 0], velocity=[0, 0], color=(255, 255, 255), mass=1, charge=0, static=False, rotation=0, interactivityType="force"):
        self.accelaration = np.array([0.0, 0.0], dtype='float64')
        self.color = color
        self.static = static
        self.selected = False

        self.mass = mass
        self.charge = charge

        self.interactivityType = interactivityType

        self.force = np.array([0.0, 0.0], dtype='float64')
        self.accelaration = np.array([0.0, 0.0], dtype='float64')
        self.accelarationAVG = np.array([0.0, 0.0], dtype='float64')

        self.torque = 0
        self.angularVelocity = 0
        self.angularAccelaration = 0
        self.interactiveTorque = 0
        
        self.interactiveForce = [0,0]

        self.lines = []
        self.lineWidth = 0
        self.circles = []
        self.polygons = []
        self.texts = []

        self.setPosition(position)
        self.setVelocity(velocity)
        self.setRotation(rotation)

    def setPosition(self, position):
        self.position = np.array(position, dtype='float64')

    def setRotation(self, angle):
        self.angle = angle
        cos = np.cos(angle)
        sin = np.sin(angle)
        self.rotationMatrix = np.array([[cos, -sin], [sin, cos]])
        self.inverseRotationMatrix = np.array([[cos, sin], [-sin, cos]])

    def setColor(self, color):
        self.color = color
        self.setShapes()

    def setShapes(self):
        pass

    def setVelocity(self, velocity):
        self.velocity = np.array(velocity, dtype='float64')

    def calculateTorque(self,force,global_grab_location):
        local_grab_location = np.array(global_grab_location) - self.position
        W = local_grab_location
        V = local_grab_location+force
        r = magnitude(W)
        perp = perpendicular_component_magnitude(V,W)
        return -r*perp
    
    def applyForce(self,force,global_grab_location):
        self.torque += -self.calculateTorque(force,global_grab_location)
        self.force += force

    def eulerODESolver(self,dt,force=[0,0],torque=0):

        self.force += np.array(force,dtype='float64')+self.interactiveForce
        self.accelaration = self.force / self.mass
        AVGlength = 10000
        self.accelarationAVG = interp(
            self.accelarationAVG, self.accelaration, 1/AVGlength)
        self.velocity += self.accelaration * dt
        self.position += self.velocity * dt

        self.torque += self.interactiveTorque + torque
        self.angularAccelaration = self.torque / self.mass
        self.angularVelocity += self.angularAccelaration * dt
        self.angle += self.angularVelocity * dt
        self.setRotation(self.angle)
        self.force = np.array([0,0],dtype='float64')
        self.torque = 0

    def createFunction(self, t, old):
        pass

    def updateInteractivity(self, screen):
        if self.static:
            GlobalCursorPosition = screen.StaticCursorPosition
            LocalCursorPosition = screen.StaticCursorPosition
            cam = screen.static_camera
        else:
            GlobalCursorPosition = screen.GlobalCursorPosition
            LocalCursorPosition = screen.LocalCursorPosition
            cam = screen.camera

        self.interactiveForce = [0, 0]
        self.interactiveTorque = 0
        if self in screen.selectedObjects:
            if not self.selected:
                self.offset = (self.position - GlobalCursorPosition)@self.inverseRotationMatrix

            self.setHoverColor()
            if screen.dragging:
                if self.interactivityType == "position":
                    self.setPosition(
                        LocalCursorPosition+cam.position+self.offset)
                    if self.selected:
                        self.velocity = (self.position-self.lasPos)/screen.dt/2
                    self.selected = True
                    self.lasPos = copy(self.position)
                if self.interactivityType == "force":
                    screen.draw(
                        Line(begin=GlobalCursorPosition, end=self.position-self.offset@self.rotationMatrix))
                    self.interactiveForce = (
                        GlobalCursorPosition-self.position + self.offset@self.rotationMatrix)*10
                    self.selected = True

                    W = self.offset@self.rotationMatrix
                    V = GlobalCursorPosition-self.position
                    r = magnitude(W)
                    perp = perpendicular_component_magnitude(V,W)
                    self.interactiveTorque = -perp*10*r

                    self.angularVelocity *= 0.99
                    self.velocity *= 0.90

            else:
                self.selected = False
        else:
            self.setStandardColor()
    
    def setHoverColor(self):
        pass

    def setStandardColor(self):
        pass

class Node(Phobject):
    def __init__(self, pos=[0, 0], vel=[0, 0], radius=0.2, color=(0, 0, 0), borderColor=(200, 200, 200), borderSize=0.3, mass=1, charge=0, interactivityType="position", static=False, rotation=0):
        super().__init__(pos, vel, color, mass, charge, static, rotation)
        self.radius = radius
        self.borderColor = borderColor
        self.borderSize = borderSize
        self.interactivityType = interactivityType
        self.setShapes()

    def setHoverColor(self):
        self.setColor((100, 100, 100))

    def setStandardColor(self):
        self.setColor((0, 0, 0))

    def setShapes(self):
        self.circles = [[self.radius, [0, 0], self.borderColor], [
            self.radius*(1-self.borderSize), [0, 0], self.color]]

    def setRadius(self, radius):
        self.radius = radius
        self.setShapes()

    def createFunction(self, t, old):
        size = calculateBezier([0, 0], [0, 3], [0.5, 1.5], [
                               1, 1], t)[1]*old.radius
        self.setRadius(size)


class Disk(Node):
    def __init__(self, *args, radius=1, interactivityType="force", **kwargs):
        super().__init__(*args, radius=radius, interactivityType=interactivityType, **kwargs)

    def setShapes(self):
        self.circles = [
            [self.radius, [0, 0], self.borderColor], 
            [self.radius/8, [self.radius*0.6, 0], self.color],
            [self.radius/16, [0.0, 0], self.color]
        ]


class Line(Phobject):
    def __init__(self, begin=[0, 0], end=[1, 0], color=(255, 255, 255), lineWidth=5, position=[0, 0]):
        super().__init__(position=position, color=color)
        self.begin = np.array(begin)
        self.end = np.array(end)
        self.lineWidth = lineWidth
        self.setShapes()

    def setShapes(self, ratio=1):
        self.lines = []
        if ratio == 1:
            self.lines.append([self.begin, self.end, self.color])
        else:
            self.lines.append(
                [self.begin, interp(self.begin, self.end, ratio), self.color])

    def setEnds(self, begin, end):
        self.begin = np.array(begin)
        self.end = np.array(end)
        self.setShapes()

    def setDirection(self, begin, direction, scale=1):
        self.setEnds(begin, begin+np.array(direction)*scale)

    def createFunction(self, t, old):
        self.setShapes(ratio=t)
