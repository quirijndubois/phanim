import pygame
import phanim.functions as pf
import numpy as np
import time

pygame.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption("Phanim window (beta)")
icon = pygame.image.load('phanim/icon.png')
pygame.display.set_icon(icon)

class Screen():
    def __init__(self,resolution,zoom = 10,fullscreen=False):
        self.resolution = resolution
        self.display = pygame.display.set_mode(resolution,flags=pygame.SCALED,vsync=1)
        self.surface = pygame.Surface(resolution,pygame.SRCALPHA)
        if fullscreen:
            self.display = pygame.display.set_mode(resolution,flags=pygame.SCALED+pygame.FULLSCREEN,vsync=1)
        self.updaterList = []
        self.t0 = time.time()
        self.clock = pygame.time.Clock()
        self.zoom = zoom
        self.pixelsPerUnit = self.resolution[0] / self.zoom

        self.mouseThightness = 0.5



    def addUpdater(self,someFunction,substeps=1):
        self.updaterList.append([someFunction,substeps])

    def drawLines(self,lines,width):
        for line in lines:
            start = pf.coords2screen(self.resolution,line[0],self.pixelsPerUnit)
            stop = pf.coords2screen(self.resolution,line[1],self.pixelsPerUnit)

            pygame.draw.line(
                self.surface,
                line[2],
                start,
                stop,
                width=width
            )


    def drawCircle(self,pos,radius,color):
            pos = pf.coords2screen(self.resolution, pos, self.pixelsPerUnit)
            pygame.draw.circle(self.surface, color, pos, radius*self.pixelsPerUnit)

    def drawPolygons(self,polygons,color):
        for polygon in polygons:
            points = []
            for point in polygon:
                points.append(pf.coords2screen(self.resolution, point, self.pixelsPerUnit))
            pygame.draw.polygon(self.surface, color, points)

    def draw(self,*args):
        for phobject in args:
            if hasattr(phobject, 'lines'):
                self.drawLines(phobject.lines, phobject.lineWidth)
            if hasattr(phobject, 'radius'):
                self.drawCircle(phobject.position,phobject.radius,phobject.color)
            if hasattr(phobject,"polygons"):
                self.drawPolygons(phobject.polygons,phobject.color)

    def run(self,background=(50,50,50)):
        running = True
        dt = 0
        pos = pygame.mouse.get_pos()

        while running:

            self.t = time.time() - self.t0

            self.zoom = self.resolution[0] / self.zoom

            self.keys = pygame.key.get_pressed()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    print("Window closed!")

            self.display.fill(background)
            self.surface.fill((0,0,0,0))

            pos = pf.interp2d(pos,pygame.mouse.get_pos(),self.mouseThightness)
            self.mousePos = pf.screen2cords(self.resolution, pos, self.pixelsPerUnit)

            for func in self.updaterList:
                for i in range(func[1]):
                    self.dt = dt/func[1]
                    func[0](self)

            self.display.blit(self.surface,(0,0))

            radius = 10
            circle = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
            pygame.draw.circle(circle, (255, 255, 255, 80), (radius, radius), radius)
            self.display.blit(circle,[pos[0]-radius,pos[1]-radius])

            pygame.display.flip()
            dt = self.clock.tick(60) / 1000
        pygame.quit()


