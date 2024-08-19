from phanim.functions import *
from phanim.group import *
from phanim.ui import *
from copy import copy

class Animation():
    
    """
    Represents an animation of a phobject.

    Attributes:
        object (Phobject): The phobject being animated.
        position (list): The position of the phobject.
        duration (int): The duration of the animation.
        currentFrame (int): The current frame of the animation.
        oldPhobject (Phobject): A copy of the original phobject.
        animationMode (str): The mode of the animation.

    Methods:
        __init__(phobject, duration, mode): Initializes the animation.
        updateAndPrint(): Updates the animation and prints the current state.
    """

    def __init__(self,phobject,duration = 60,mode = "smoothstep"):
        self.object = phobject
        self.position = phobject.position
        self.duration = duration
        self.currentFrame = 0
        self.oldPhobject = copy(phobject)
        self.animationMode = mode
    def updateAndPrint(self):
        """
        Updates the animation and prints the current state.

        This method updates the animation based on the current frame and the animation mode.
        It then updates the object's attributes and prints the current state of the animation.

        Parameters:
            None

        Returns:
            None
        """
        
        t = self.currentFrame / self.duration
        if self.animationMode == "smoothstep":
            self.t = interp(t**2,np.sqrt(t),t)
        if self.animationMode == "smooth":
            a = interp(0,1,t)
            b = interp(0,a,t)
            c = interp(a,1,t)
            self.t = interp(b,c,t)
        if self.animationMode == "linear":
            self.t = t
        self.update()

        if hasattr(self,"object"):
            if hasattr(self.object,"groupObjects"):
                for obj in self.object.groupObjects:
                    self.groupObjects = self.object.groupObjects
            else:
                self.__setAttributes(self.object)

    def __setAttributes(self,obj):
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
    """
    Represents a create animation.

    Attributes:
        mode (str): The mode of the create animation.

    Methods:
        update(): Updates the create animation.
    """
    mode = "add"
    def update(self):
        self.object.createFunction(self.t,self.oldPhobject)

class Destroy(Animation):
    """
    Represents a destroy animation.

    Attributes:
        mode (str): The mode of the destroy animation.

    Methods:
        update(): Updates the destroy animation.
    """
    mode = "remove"
    def update(self):
        self.object.createFunction(1-self.t,self.oldPhobject)

class Transform(Animation):
    """
    Represents a transformation animation.

    Attributes:
        newPhobject (Phobject): The new phobject to transform into.
        duration (int): The duration of the animation.
        mode (str): The mode of the animation.

    Methods:
        __init__(phobject, newPhobject, duration, mode): Initializes the animation.
        update(): Updates the animation.

    Args:
        phobject (Phobject): The phobject to transform.
        newPhobject (Phobject): The new phobject to transform into.
        duration (int): The duration of the animation.
        mode (str): The mode of the animation.
    """
    mode = None
    def __init__(self,phobject,newPhobject,duration=60,mode = "smooth"):
        super().__init__(phobject,duration, mode)
        self.newPhobject = newPhobject
    
    def update(self):
        self.object.transformFunction(self.t,self.oldPhobject,self.newPhobject)
        self.object.position = interp(self.oldPhobject.position,self.newPhobject.position,self.t)


class Add(Animation):
    """
    Represents an add animation.

    Attributes:
        mode (str): The mode of the animation.

    Methods:
        __init__(phobject, mode): Initializes the animation.

    Args:
        phobject (Phobject): The phobject to add.
        mode (str): The mode of the animation.
    """

    mode = "add"
    def __init__(self, phobject,mode = "smooth"):
        super().__init__(phobject,1, mode)

class Remove(Animation):
    """
    Represents a remove animation.

    Attributes:
        mode (str): The mode of the animation.

    Methods:
        __init__(phobject, mode): Initializes the animation.

    Args:
        phobject (Phobject): The phobject to remove.
        mode (str): The mode of the animation.
    """
    mode = "remove"
    def __init__(self, phobject,mode = "smooth"):
        super().__init__(phobject,1, mode)

class Sleep(Animation):
    """
    Represents a sleep animation.

    Attributes:
        duration (int): The duration of the sleep animation.

    Methods:
        __init__(duration): Initializes the sleep animation.

    Args:
        duration (int): The duration of the sleep animation.
    """
    mode = None
    def __init__(self,duration):
        self.animationMode = "linear"
        self.object = None
        self.duration = duration
        self.currentFrame = 0

class Move(Animation):
    """
    Represents a move animation.

    Attributes:
        object (Phobject): The phobject to move.

    Methods:
        update(): Updates the move animation.

    Args:
        phobject (Phobject): The phobject to move.
    """
    mode = None
    def __init__(self, phobject, target, duration=60,mode = "smooth"):
        super().__init__(phobject, duration, mode)
        self.target = target
    
    def update(self):
        self.object.setPosition(interp(self.oldPhobject.position,self.target,self.t))

class Shift(Move):  
    """
    Represents a shift animation.

    Methods:
        update(): Updates the shift animation.
    """  
    def update(self):
        self.object.setPosition(interp(self.oldPhobject.position,self.oldPhobject.position+self.target,self.t))    
    
class AnimateValue(Animation):
    """
    Represents an animation of a value.

    Attributes:
        function (function): The function to animate.
        target (object): The target of the animation.
        duration (int): The duration of the animation.
        currentFrame (int): The current frame of the animation.
        animationMode (str): The mode of the animation.

    Methods:
        __init__(function, target, duration, mode): Initializes the animation.
        update(): Updates the animation.
    """
    mode = None
    def __init__(self,function,target,duration = 60,mode = "smooth"):
        self.duration = duration
        self.currentFrame = 0
        self.animationMode = mode
        self.function = function
        self.target = target
    
    def update(self):
        self.function(interp(self.target[0],self.target[1],self.t))

class laggedStart():
    """
    Represents a lagged start animation.

    Attributes:
        animations (list): The list of animations.
        playingAnimations (list): The list of playing animations.
        currentFrame (int): The current frame of the animation.
        lagRatio (float): The lag ratio of the animation.

    Methods:
        __init__(*args, lagRatio): Initializes the animation.
        updateAndPrint(): Updates the animation and prints the current state.
        __setDuration(): Sets the duration of the animation.
    """
    mode = "wrapper"
    def __init__(self,*args,lagRatio = 0.1):
        self.animations = args
        self.playingAnimations = [self.animations[0]]
        self.currentFrame = 0
        self.lagRatio = lagRatio
        self.__setDuration()
    
    def updateAndPrint(self):
        if self.playingAnimations[-1].currentFrame/self.playingAnimations[-1].duration > self.lagRatio:
            if len(self.playingAnimations)<len(self.animations):
                self.playingAnimations.append(self.animations[len(self.playingAnimations)])

        for animation in self.playingAnimations:
            animation.updateAndPrint()
            if animation.currentFrame < animation.duration:
                animation.currentFrame +=1
    
    def __setDuration(self):
        self.duration = 0
        for animation in self.animations:
            self.duration+=animation.duration*self.lagRatio
        self.duration += self.animations[-1].duration*(1-self.lagRatio)
        self.duration = int(self.duration)+len(self.animations)


def makeGrid(n_horizontal=8,n_vertical=5):
    grids = DGrid(n_horizontal=n_horizontal,n_vertical=n_vertical).groupObjects
    animations = []
    for grid in grids:
        for line in grid.lines:
            animations.append(Create(
                Line(start=grid.position+line[0],stop=grid.position+line[1],lineWidth=grid.lineWidth,color=line[2]),
                duration=30
                ))
    return laggedStart(*animations,lagRatio=0.01)



