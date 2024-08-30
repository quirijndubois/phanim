import numpy as np
from copy import deepcopy
from phanim.group import Group
from .phobject import *
from .functions import *


class Slider(Group):
    def __init__(self, value=None, width=2, position=[0, 0], color=(150, 150, 230), maxValue=1, minValue=0, static=False):
        self.width = width
        self.position = np.array(position)
        self.selected = False
        if value == None:
            self.value = interp(minValue, maxValue, 0.5)
        else:
            self.value = value

        self.color = color
        self.maxValue = maxValue
        self.minValue = minValue
        self.static = static

        self.setPhobjects()

    def setPhobjects(self):
        self.groupObjects = [
            Line(
                start=[self.position[0]-self.width/2, self.position[1]],
                stop=[self.position[0]+self.width/2, self.position[1]],
                color=self.color,
            ),
            Node(
                pos=self.position+interp(np.array([-self.width/2, 0]), np.array(
                    [self.width/2, 0]), (self.value-self.minValue)/(self.maxValue-self.minValue)),
                borderColor=self.color,
            ),
        ]

    def updateInteractivity(self, screen):

        if self.static:
            CursorPosition = screen.LocalCursorPosition
        else:
            CursorPosition = screen.GlobalCursorPosition

        if self in screen.selectedObjects:
            if not self.selected:
                self.offset = self.groupObjects[1].position - \
                    CursorPosition
            if len(self.color) == 3:
                self.groupObjects[1].setColor(
                    (self.color[0]/3, self.color[1]/3, self.color[2]/3)
                )
            if screen.dragging:
                maximimPos = self.position[0]+self.width/2
                minimumPos = self.position[0]-self.width/2
                self.groupObjects[1].setPosition(
                    [clamp((CursorPosition+self.offset)[0],
                           minimumPos, maximimPos), self.position[1]]
                )
                self.value = interp(self.minValue, self.maxValue, ((
                    self.groupObjects[1].position[0]-self.position[0])/(self.width/2)+1)/2)
                self.selected = True
            else:
                self.selected = False
        else:
            self.groupObjects[1].setColor((0, 0, 0))

    def checkSelection(self, screen):

        if self.static:
            CursorPosition = screen.StaticCursorPosition
            camera = screen.static_camera
        else:
            CursorPosition = screen.LocalCursorPosition
            camera = screen.camera

        if magnitude(self.groupObjects[1].position-(CursorPosition+camera.position)) < self.groupObjects[1].radius:
            return True
        else:
            return False

    def setValue(self, value):
        self.value = clamp(value, self.minValue, self.maxValue)
        self.groupObjects[1].setPosition(self.position+interp([-self.width/2, 0], [
                                         self.width/2, 0], (self.value-self.minValue)/(self.maxValue-self.minValue)))

    def setPosition(self, position):
        self.position = position
        self.setPhobjects()
