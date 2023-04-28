from . import functions as pf
from copy import deepcopy
import math

class Animation():
    def __init__(self,phobject,duration = 60,mode = "smoothstep"):
        self.object = phobject
        self.duration = duration
        self.currentFrame = 0
        self.oldPhobject = deepcopy(phobject)
        self.animationMode = mode
    def updateAndPrint(self):
        t = self.currentFrame / self.duration
        if self.animationMode == "smoothstep":
            self.t = pf.interp(t**2,math.sqrt(t),t)
        if self.animationMode == "smooth":
            a = pf.interp(0,1,t)
            b = pf.interp(0,a,t)
            c = pf.interp(a,1,t)
            self.t = pf.interp(b,c,t)
        if self.animationMode == "linear":
            self.t = t
        self.update()

        if hasattr(self,"object"):
            if hasattr(self.object,"groupObjects"):
                for obj in self.object.groupObjects:
                    self.groupObjects = deepcopy(self.object.groupObjects)
            else:
                self.setAttributes(self.object)

    def setAttributes(self,obj):
        if hasattr(self.object, 'lines'):
            self.lines = self.object.lines
            self.lineWidth = self.object.lineWidth
        if hasattr(self.object, 'circles'):
            self.circles = self.object.circles
        if hasattr(self.object,"polygons"):
            self.polygons = self.object.polygons
            self.color =self.object.color
        if hasattr(self.object, "texts"):
            self.texts = self.object.texts

    def update(self):
        pass


class Create(Animation):
    mode = "add"
    def update(self):
        self.object.createFunction(self.t,self.oldPhobject)

class Destroy(Animation):
    mode = "remove"
    def update(self):
        self.object.createFunction(1-self.t,self.oldPhobject)

class Transform(Animation):
    mode = None
    def __init__(self,phobject,newPhobject,duration=60,mode = "smooth"):
        super().__init__(phobject,duration, mode)
        self.newPhobject = newPhobject
    
    def update(self):
        self.object.transformFunction(self.t,self.oldPhobject,self.newPhobject)


class Add(Animation):
    mode = "add"
    def __init__(self, phobject,mode = "smooth"):
        super().__init__(phobject,1, mode)

class Remove(Animation):
    mode = "remove"
    def __init__(self, phobject,mode = "smooth"):
        super().__init__(phobject,1, mode)

class Sleep(Animation):
    mode = None
    def __init__(self,duration):
        self.animationMode = "linear"
        self.object = None
        self.duration = duration
        self.currentFrame = 0

class Move(Animation):
    mode = None
    def __init__(self, phobject, target, duration=60,mode = "smooth"):
        super().__init__(phobject, duration, mode)
        self.target = target
        # self.oldPosition = deepcopy(phobject.position)
    
    def update(self):
        self.object.setPosition(pf.interp2d(self.oldPhobject.position,self.target,self.t))
    
class AnimateValue(Animation):
    mode = None
    def __init__(self,function,target,duration = 60,mode = "smooth"):
        self.duration = duration
        self.currentFrame = 0
        self.animationMode = mode
        self.function = function
        self.target = target
    
    def update(self):
        self.function(pf.interp(self.target[0],self.target[1],self.t))




