import pygame
from . import functions as pf
from . camera import *
from . animate import *
import numpy as np
import time
from copy import deepcopy
from pygame import gfxdraw

pygame.init()
pygame.mouse.set_visible(False)
pygame.display.set_caption("Phanim window (beta)")
icon = pygame.image.load('phanim/icon.png')
pygame.display.set_icon(icon)

class Screen():
    def __init__(self,resolution=(0,0),zoom = 10,fullscreen=False,background=(10,15,20),fontSize=0.5,panning=False):

        infoObject = pygame.display.Info()

        if resolution == (0,0):
            self.resolution = (infoObject.current_w, infoObject.current_h)
        else:
            self.resolution = resolution

        self.camera = Camera(zoom,self.resolution)

        self.surface = pygame.Surface(self.resolution,pygame.SRCALPHA)
        self.fontSize = int(fontSize*self.camera.pixelsPerUnit)
        self.font = pygame.font.SysFont(None,self.fontSize)

        self.panning = panning

        if fullscreen:
            self.display = pygame.display.set_mode(self.resolution,pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.display = pygame.display.set_mode(self.resolution,flags=pygame.SCALED,vsync=1)

        self.updaterList = []
        self.mouseClickUpdaterList = []
        self.mouseDragUpdaterList = []
        self.mouseDownUpdaterList = []
        self.animationQueue = []
        self.drawList = []
        self.t0 = time.time()
        self.clock = pygame.time.Clock()
        self.background = background
        self.dragging = False
        self.mouseButtonDown = False
        self.scroll = [0,0]
        self.lastScroll = [0,0]

        self.mouseThightness = 0.4



    def addUpdater(self,someFunction,substeps=1):
        self.updaterList.append([someFunction,substeps])

    def addMouseClickUpdater(self,someFunction):
        self.mouseClickUpdaterList.append(someFunction)
    
    def addMouseDownUpdater(self,someFunction):
        self.mouseDownUpdaterList.append(someFunction)

    def addMouseDragUpdater(self,someFunction):
        self.mouseDragUpdaterList.append(someFunction)

    def handlePanning(self,mouseDown,dragging):
        if mouseDown:
            self.panBeginCameraPosition = self.camera.position
            self.panBeginMousePos = self.mousePos
        if dragging:
            self.camera.setPosition(pf.vadd(
                pf.diff(self.panBeginMousePos,self.mousePos),
                self.panBeginCameraPosition
            ))

        scroll = self.scroll
        if abs(scroll[0]) == 1:
            scroll[0] = 0
        if abs(scroll[1]) == 1:
            scroll[1] = 0
        scroll[0] /= 30
        scroll[1] /= 30
        self.camera.setZoom(self.camera.zoom - self.camera.zoom*scroll[1])

    def drawLines(self,lines,width,position):
        for line in lines:
            start = self.camera.coords2screen(pf.vadd(line[0],position))
            stop = self.camera.coords2screen(pf.vadd(line[1],position))

            pixelWidth = int(width/self.camera.zoom*20)
            if pixelWidth < 1:
                pixelWidth = 1

            if len(line) == 3:
                color = line[2]
            else:
                color = (255,255,255)
            pygame.draw.line(
                self.surface,
                color,
                start,
                stop,
                width=pixelWidth
            )


    def drawCircles(self,circles,position):
            for circle in circles:
                pos = self.camera.coords2screen(pf.vadd(circle[1],position))
                pygame.draw.circle(self.surface, circle[2], pos, circle[0]*self.camera.pixelsPerUnit)

    def drawPolygons(self,polygons,color,position):
        for polygon in polygons:
            points = []
            for point in polygon:
                points.append(self.camera.coords2screen(pf.vadd(point,position)))
            pygame.draw.polygon(self.surface, color, points)

    def drawText(self,texts,position):
        for text in texts:
            if len(text) > 0:
                img = self.font.render(text[0],True,text[2])
                pos = self.camera.coords2screen(pf.vadd(text[1],position))
                self.display.blit(img,pos)

    def drawPhobject(self,phobject):
        if hasattr(phobject, 'circles'):
            self.drawCircles(phobject.circles, phobject.position)
        if hasattr(phobject, 'lines'):
            self.drawLines(phobject.lines, phobject.lineWidth, phobject.position)
        if hasattr(phobject,"polygons"):
            self.drawPolygons(phobject.polygons,phobject.color, phobject.position)
        if hasattr(phobject, "texts"):
            self.drawText(phobject.texts, phobject.position)

    def draw(self,*args):
        for arg in args:
            if hasattr(arg,"groupObjects"):
                for phobject in arg.groupObjects:
                    self.drawPhobject(phobject)
            else:
                self.drawPhobject(arg)


    def handleInput(self):
            self.keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    print("Window closed!")
                if event.type == pygame.MOUSEBUTTONUP:
                    self.dragging = False
                    for func in self.mouseClickUpdaterList:
                        func(self)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.dragging = True
                    self.mouseButtonDown = True
                    for func in self.mouseDownUpdaterList:
                        func(self)
                if event.type == pygame.MOUSEWHEEL:
                    self.scroll = [event.x,event.y]
            
            if self.dragging:
                for func in self.mouseDragUpdaterList:
                    func(self)

    def resetDisplay(self):
            self.display.fill(self.background)
            self.surface.fill((0,0,0,0))

    
    def calculateCursor(self):
        pos = pygame.mouse.get_pos()
        pos = pf.interp2d(pos,pygame.mouse.get_pos(),self.mouseThightness)
        self.cursorPositionScreen = pos
        self.cursorPosition = self.camera.screen2cords(pos)
        self.mousePos = self.cursorPosition #for version compatibility

    def performUpdateList(self):
        for func in self.updaterList:
            for i in range(func[1]):
                self.dt = self.frameDt/func[1]
                func[0](self)

    def drawCursor(self):
        radius = 10
        circle = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(circle, (150, 150, 150, 120), (radius, radius), radius)
        self.display.blit(circle,[self.cursorPositionScreen[0]-radius,self.cursorPositionScreen[1]-radius])

    def play(self,*args):
        self.animationQueue.append(list(args))

    def wait(self,duration):
        self.play(Sleep(duration))

    def playAnimations(self):
        if len(self.animationQueue) > 0:
            for index,animation in enumerate(self.animationQueue[0]):
                if animation.currentFrame == 0:
                    if hasattr(animation,"object"):
                        animation.oldPhobject = deepcopy(animation.object)
                animation.currentFrame += 1
                animation.updateAndPrint()
                if animation.mode == "add":
                    self.draw(animation)
                if animation.currentFrame == animation.duration:
                    if animation.mode == "add":
                        self.add(animation.object)
                    if animation.mode == "remove":
                        self.remove(animation.object)
                    self.animationQueue[0].pop(index)
            if len(self.animationQueue[0]) == 0:
                self.animationQueue.pop(0)

        
    def add(self,phobject):
        self.drawList.append(phobject)

    def remove(self,phobject):
        self.drawList.remove(phobject)
        
    def drawDrawList(self):
        self.draw(*self.drawList)

    def run(self):
        self.frameDt = 0
        self.running = True
        while self.running:
            self.t = time.time() - self.t0

            self.handleInput()
            self.resetDisplay()
            self.calculateCursor()
            self.drawDrawList()
            self.playAnimations()
            if self.panning:
                self.handlePanning(self.mouseButtonDown,self.dragging)
            self.performUpdateList()

            self.display.blit(self.surface,(0,0))
            self.drawCursor()

            pygame.display.update()
            self.frameDt = self.clock.tick(60) / 1000

            self.mouseButtonDown = False #because this should only be True for a single frame

        pygame.quit()