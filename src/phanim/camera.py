from . import functions as pf
import numpy as np

class Camera():
    def __init__(self,zoom,resolution,position = [0,0],rotation = 0):
        self.zoom = zoom
        self.resolution = resolution
        self.position = position
        self.rotation = rotation
        self.aspectRatio = self.resolution[0]/self.resolution[1]
        self.pixelsPerUnit = self.resolution[1] / self.zoom
        self.__calculateBounds()


    def coords2screen(self,location):
        # x = location[0] - self.position[0]
        # y = location[1] - self.position[1]
        # a = self.rotation
        # if a < 0.01 and a > -0.01:
        #     newLocation = [
        #         x*np.cos(a) - y*np.sin(a),
        #         x*np.sin(a) + y*np.cos(a),
        #     ]
        # else:
        # newLocation = [x,y]
        newLocation = pf.diff(location,self.position)

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
        self.__calculateBounds()
    
    def setZoom(self,zoom):
        self.zoom = zoom
        if self.zoom < 0.1:
            self.zoom = 0.1
        if self.zoom > 1000:
            self.zoom = 1000
        self.pixelsPerUnit = self.resolution[1] / self.zoom
        self.__calculateBounds()

    def __calculateBounds(self):
        self.bounds = [
            [self.position[0]-self.zoom/2*self.aspectRatio,self.position[0]+self.zoom/2*self.aspectRatio],
            [self.position[1]-self.zoom/2,self.position[1]+self.zoom/2]
        ]
