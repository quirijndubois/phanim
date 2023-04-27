from . import functions as pf
import numpy as np

class Camera():
    def __init__(self,zoom,resolution,position = [0,0],rotation = 0):
        self.zoom = zoom
        self.resolution = resolution
        self.position = position
        self.rotation = rotation
        self.pixelsPerUnit = self.resolution[0] / self.zoom

    def coords2screen(self,location):
        x = location[0] - self.position[0]
        y = location[1] - self.position[1]
        a = self.rotation
        if a < 0.01 and a > -0.01:
            newLocation = [
                x*np.cos(a) - y*np.sin(a),
                x*np.sin(a) + y*np.cos(a),
            ]
        else:
            newLocation = [x,y]

        return pf.coords2screen(self.resolution,newLocation, self.pixelsPerUnit)
    
    def screen2cords(self,location):
        x = location[0] - self.position[0]
        y = location[1] - self.position[1]
        a = self.rotation
        newLocation = [
            x*np.cos(a) - y*np.sin(a),
            x*np.sin(a) + y*np.cos(a),
        ]
        return pf.screen2cords(self.resolution,newLocation, self.pixelsPerUnit)
    
    def setPosition(self,position):
        self.position = position
    
    def setZoom(self,zoom):
        self.zoom = zoom
        self.pixelsPerUnit = self.resolution[0] / self.zoom