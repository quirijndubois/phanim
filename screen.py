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
    def __init__(self,resolution,zoom = 10,fullscreen=False,background=(10,15,20),fontSize=0.5):
        infoObject = pygame.display.Info()

        if resolution == 0:
            self.resolution = (infoObject.current_w, infoObject.current_h)
        else:
            self.resolution = resolution    

        self.zoom = zoom
        self.pixelsPerUnit = self.resolution[0] / self.zoom
        self.surface = pygame.Surface(self.resolution,pygame.SRCALPHA)
        self.fontSize = int(fontSize*self.pixelsPerUnit)
        self.font = pygame.font.SysFont(None,self.fontSize)

        if fullscreen:
            self.display = pygame.display.set_mode(self.resolution,pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.display = pygame.display.set_mode(self.resolution,flags=pygame.SCALED,vsync=1)

        self.updaterList = []
        self.mouseClickUpdaterList = []
        self.mouseDragUpdaterList = []
        self.t0 = time.time()
        self.clock = pygame.time.Clock()
        self.background = background
        self.dragging = False

        self.mouseThightness = 0.4



    def addUpdater(self,someFunction,substeps=1):
        self.updaterList.append([someFunction,substeps])

    def addMouseClickUpdater(self,someFunction):
        self.mouseClickUpdaterList.append(someFunction)

    def addMouseDragUpdater(self,someFunction):
        self.mouseDragUpdaterList.append(someFunction)

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


    def drawCircles(self,circles):
            for circle in circles:
                pos = pf.coords2screen(self.resolution, circle[1], self.pixelsPerUnit)
                pygame.draw.circle(self.surface, circle[2], pos, circle[0]*self.pixelsPerUnit)

    def drawPolygons(self,polygons,color):
        for polygon in polygons:
            points = []
            for point in polygon:
                points.append(pf.coords2screen(self.resolution, point, self.pixelsPerUnit))
            pygame.draw.polygon(self.surface, color, points)

    def drawText(self,texts):
        for text in texts:
            img = self.font.render(text[0],True,text[2])
            pos = pf.coords2screen(self.resolution,text[1],self.pixelsPerUnit)
            self.display.blit(img,pos)

    def draw(self,*args):
        for phobject in args:
            if hasattr(phobject, 'lines'):
                self.drawLines(phobject.lines, phobject.lineWidth)
            if hasattr(phobject, 'circles'):
                self.drawCircles(phobject.circles)
            if hasattr(phobject,"polygons"):
                self.drawPolygons(phobject.polygons,phobject.color)
            if hasattr(phobject, "texts"):
                self.drawText(phobject.texts)

    def run(self):
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
                if event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                    for func in self.mouseClickUpdaterList:
                        func(self)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.dragging = True
            
            if self.dragging:
                for func in self.mouseDragUpdaterList:
                    func(self)

            self.display.fill(self.background)
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


