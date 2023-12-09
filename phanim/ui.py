import numpy as np
from copy import deepcopy
from phanim.group import Group
from .phobject import *
from .functions import *

class Slider(Group):
    def __init__(self,value=0.5,width=2,position=[0,0],color = (150,150,230),maxValue=1,minValue=0):
        self.width=width
        self.position = position
        self.selected = False
        self.value = value
        self.color = color
        self.maxValue = maxValue
        self.minValue = minValue
        self.setPhobjects()

    def setPhobjects(self):
        self.groupObjects = [
            Line(
                start=[self.position[0]-self.width/2,self.position[1]],
                stop=[self.position[0]+self.width/2,self.position[1]],
                color=self.color,
                ),
            Node(
                pos=vadd(self.position,interp2d([-self.width/2,0],[self.width/2,0],(self.value-self.minValue)/(self.maxValue-self.minValue))),
                borderColor = self.color,
                ),
        ]

    def updateInteractivity(self,screen):
        if self in screen.selectedObjects:
            if not self.selected:
                self.offset = -pf.diff(screen.GlobalCursorPosition,self.groupObjects[1].position)
            if len(self.color) == 3:
                self.groupObjects[1].setColor(
                    (self.color[0]/3,self.color[1]/3,self.color[2]/3)
                    )
            if screen.dragging:
                maximimPos = self.position[0]+self.width/2
                minimumPos = self.position[0]-self.width/2
                self.groupObjects[1].setPosition(
                    [pf.clamp(pf.vadd(screen.GlobalCursorPosition,self.offset)[0],minimumPos,maximimPos),self.position[1]]
                    )
                self.value = interp(self.minValue,self.maxValue,((self.groupObjects[1].position[0]-self.position[0])/(self.width/2)+1)/2)
                self.selected = True
            else:
                self.selected = False
        else:
            self.groupObjects[1].setColor((0,0,0))
    
    def checkSelection(self,screen):
        if pf.magnitude(pf.diff(self.groupObjects[1].position,pf.vadd(screen.mousePos,screen.camera.position))) < self.groupObjects[1].radius:
            return True
            print(selected)
        else:
            return False
    
    def setPosition(self,position):
        self.position = position
        self.setPhobjects()