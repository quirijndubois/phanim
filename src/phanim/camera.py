from . import functions as pf
import numpy as np


class Camera():
    def __init__(self, zoom, resolution, position=[0, 0], rotation=0):
        self.zoom = zoom
        self.resolution = resolution
        self.position = np.array(position)
        self.rotation = rotation
        self.aspectRatio = self.resolution[0]/self.resolution[1]
        self.pixelsPerUnit = self.resolution[1] / self.zoom
        self.__calculateBounds()

    def coords2screen(self, location):
        newLocation = location - self.position
        return pf.coords2screen(self.resolution, newLocation, self.pixelsPerUnit)

    def screen2coords(self, location):
        return pf.screen2cords(self.resolution, location, self.pixelsPerUnit)

    def setPosition(self, position):
        self.position = np.array(position)
        self.__calculateBounds()

    def setZoom(self, zoom):
        self.zoom = zoom
        if self.zoom < 0.1:
            self.zoom = 0.1
        if self.zoom > 1000:
            self.zoom = 1000
        self.pixelsPerUnit = self.resolution[1] / self.zoom
        self.__calculateBounds()

    def __calculateBounds(self):
        self.bounds = np.array([
            [self.position[0]-self.zoom/2*self.aspectRatio,
                self.position[0]+self.zoom/2*self.aspectRatio],
            [self.position[1]-self.zoom/2, self.position[1]+self.zoom/2]
        ])
