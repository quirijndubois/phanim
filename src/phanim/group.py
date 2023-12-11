from phanim import *
from phanim.phobject import Grid

class Group():
    def __init__(self,*objects):
        self.groupObjects = objects
        self.position = [0,0]
    
    def createFunction(self,t,old):
        for i in range(len(self.groupObjects)):
            self.groupObjects[i].createFunction(t,old.groupObjects[i])

class DGrid(Group):
    def __init__(self,Xspacing=1,Yspacing=1,n_horizontal=10,n_vertical=10,color=(80,80,80),color2=(40,40,40)):
        self.groupObjects = [
            Grid(Xspacing,Yspacing,n_horizontal,n_vertical,position=[0.5,0.5],color=color2),
            Grid(Xspacing,Yspacing,n_horizontal,n_vertical,color=color)
        ]
        self.position = [0,0]