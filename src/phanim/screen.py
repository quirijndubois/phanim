import platform
import pygame
from . import functions as pf
from . camera import *
from . animate import *
import numpy as np
import time
from copy import deepcopy
import threading
from IPython import start_ipython
import os,sys

class Screen():

    os.environ['SDL_VIDEO_WINDOW_POS'] = '0,0'
    os.environ['SDL_VIDEO_FULLSCREEN_DISPLAY'] = '0'
    pygame.init()
    pygame.mouse.set_visible(False)
    pygame.display.set_caption("Phanims")
    # pygame.display.set_icon(pygame.image.load('phanim/icon.png'))

    def __init__(self,resolution=None,zoom = 10,fullscreen=False,background=(10,15,20),fontSize=0.5,panning=False):

        infoObject = pygame.display.Info()
        if resolution == None:
            self.resolution = (infoObject.current_w, infoObject.current_h)
        else:
            self.resolution = resolution

        self.camera = Camera(zoom,self.resolution)
        self.surface = pygame.Surface(self.resolution,pygame.SRCALPHA)
        self.fontSize = int(fontSize*self.camera.pixelsPerUnit)
        self.font = pygame.font.SysFont(None,self.fontSize)

        if fullscreen:
            self.display = pygame.display.set_mode(self.resolution,pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.display = pygame.display.set_mode(self.resolution,flags=pygame.SCALED,vsync=1)
        
        #Setting static settings
        self.panning = panning
        self.background = background
        self.mouseThightness = 0.4

        #preparing lists
        self.updaterList = []
        self.mouseClickUpdaterList = []
        self.mouseDragUpdaterList = []
        self.mouseDownUpdaterList = []
        self.interativityList = []
        self.animationQueue = []
        self.drawList = []
        self.selectedObjects = []

        #presetting dynamic variables
        self.dragging = False
        self.mouseButtonDown = False
        self.t0 = time.time()
        self.clock = pygame.time.Clock()
        self.scroll = [0,0]
        self.lastScroll = [0,0]

    def addUpdater(self,someFunction,substeps=1):
        self.updaterList.append([someFunction,substeps])

    def addMouseClickUpdater(self,someFunction):
        self.mouseClickUpdaterList.append(someFunction)
    
    def addMouseDownUpdater(self,someFunction):
        self.mouseDownUpdaterList.append(someFunction)

    def addMouseDragUpdater(self,someFunction):
        self.mouseDragUpdaterList.append(someFunction)

    def __handlePanning(self,mouseDown,dragging):
        if len(self.selectedObjects)>0:
            dragging = False
        if mouseDown:
            self.panBeginCameraPosition = self.camera.position
            self.panBeginMousePos = self.mousePos
        if dragging:
            self.camera.setPosition(pf.vadd(
                pf.diff(self.panBeginMousePos,self.mousePos),
                self.panBeginCameraPosition
            ))

        scroll = self.scroll
        if platform.system() == "Darwin":
            if abs(scroll[0]) == 1:
                scroll[0] = 0
            if abs(scroll[1]) == 1:
                scroll[1] = 0
        scroll[0] /= 30
        scroll[1] /= 30
        self.camera.setZoom(self.camera.zoom - self.camera.zoom*scroll[1])

    def __drawLines(self,lines,width,position):
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


    def __drawCircles(self,circles,position):
            for circle in circles:
                pos = self.camera.coords2screen(pf.vadd(circle[1],position))
                pygame.draw.circle(self.surface, circle[2], pos, circle[0]*self.camera.pixelsPerUnit)

    def __drawPolygons(self,polygons,color,position):
        for polygon in polygons:
            points = []
            for point in polygon:
                points.append(self.camera.coords2screen(pf.vadd(point,position)))
            pygame.draw.polygon(self.surface, color, points)

    def __drawText(self,texts,position):
        for text in texts:
            if len(text) > 0:
                img = self.font.render(text[0],True,text[2])
                pos = self.camera.coords2screen(pf.vadd(text[1],position))
                self.display.blit(img,pos)

    def __drawPhobject(self,phobject):
        if hasattr(phobject, 'circles'):
            self.__drawCircles(phobject.circles, phobject.position)
        if hasattr(phobject, 'lines'):
            self.__drawLines(phobject.lines, phobject.lineWidth, phobject.position)
        if hasattr(phobject,"polygons"):
            self.__drawPolygons(phobject.polygons,phobject.color, phobject.position)
        if hasattr(phobject, "texts"):
            self.__drawText(phobject.texts, phobject.position)

    def draw(self,*args):
        for arg in args:
            if hasattr(arg,"groupObjects"):
                for phobject in arg.groupObjects:
                    self.__drawPhobject(phobject)
            else:
                self.__drawPhobject(arg)

    def makeInteractive(self,*args):
        for arg in args:
            if type(arg) is list:
                for phobject in arg:
                    self.interativityList.append(phobject)
            else:
                self.interativityList.append(arg)

    
    def __handleInteractivity(self):
        if not self.dragging:
            self.selectedObjects = []
            for phobject in self.interativityList:
                if hasattr(phobject,"radius"):
                    if pf.magnitude(pf.diff(phobject.position,pf.vadd(self.mousePos,self.camera.position))) < phobject.radius:
                        self.selectedObjects.append(phobject)
                elif hasattr(phobject,"checkSelection"):
                    if phobject.checkSelection(self):
                        self.selectedObjects.append(phobject)
                elif hasattr(phobject,"groupObjects"):
                    for phobject2 in phobject.groupObjects:
                        if hasattr(phobject2,"radius"):
                            if pf.magnitude(pf.diff(phobject2.position,pf.vadd(self.mousePos,self.camera.position))) < phobject2.radius:
                                self.selectedObjects.append(phobject2)

        for phobject in self.interativityList:
            if hasattr(phobject,"updateInteractivity"):
                phobject.updateInteractivity(self)

    def __handleInput(self):
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

    def __resetDisplay(self):
            self.display.fill(self.background)
            self.surface.fill((0,0,0,0))

    def __calculateCursor(self):
        pos = pygame.mouse.get_pos()
        pos = pf.interp2d(pos,pygame.mouse.get_pos(),self.mouseThightness)
        self.cursorPositionScreen = pos
        self.LocalcursorPosition = self.camera.screen2cords(pos)
        self.GlobalCursorPosition = vadd(self.LocalcursorPosition,self.camera.position)
        self.mousePos = self.LocalcursorPosition #for version compatibility (should be discontinued)

    def __performUpdateList(self):
        if self.t > 1:
            for func in self.updaterList:
                for i in range(func[1]):
                    self.dt = self.frameDt/func[1]
                    func[0](self)

    def __drawCursor(self):
        radius = 10
        circle = pygame.Surface((radius*2, radius*2), pygame.SRCALPHA)
        pygame.draw.circle(circle, (150, 150, 150, 120), (radius, radius), radius)
        self.display.blit(circle,[self.cursorPositionScreen[0]-radius,self.cursorPositionScreen[1]-radius])

    def play(self,*args):
        self.animationQueue.append(list(args))

    def wait(self,duration):
        self.play(Sleep(duration))

    def __playAnimations(self):
        if len(self.animationQueue) > 0:
            for index,animation in enumerate(self.animationQueue[0]):

                if animation.mode == "wrapper":
                    animation.currentFrame+=1
                    self.__drawWrapperAnimation(animation)
                    animation.updateAndPrint()

                    if animation.currentFrame == animation.duration:
                        for wrappedAnimation in animation.animations:
                            if wrappedAnimation.mode == "add":
                                self.add(wrappedAnimation.object)
                            if wrappedAnimation.mode == "remove":
                                self.remove(wrappedAnimation.object)


                else:
                    self.__drawAnimation(animation)

                if animation.currentFrame == animation.duration:
                    self.animationQueue[0].pop(index)

            if len(self.animationQueue[0]) == 0:
                self.animationQueue.pop(0)
        
    def __drawAnimation(self,animation):
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
    
    def __drawWrapperAnimation(self,animation):
        for index,wrappedAnimation in enumerate(animation.animations):
            if wrappedAnimation.currentFrame == 0:
                if hasattr(wrappedAnimation,"object"):
                    wrappedAnimation.oldPhobject = deepcopy(wrappedAnimation.object)
            if wrappedAnimation.mode == "add":
                self.draw(wrappedAnimation)
                

        
    def add(self,phobject):
        self.drawList.append(phobject)

    def remove(self,phobject):
        self.drawList.remove(phobject)
    
    def __drawDrawList(self):
        self.draw(*self.drawList)

    def run_interactive(self,globals):
        def thread_loop():
            start_ipython(argv=[], user_ns=globals)

        print_thread = threading.Thread(target=thread_loop)
        print_thread.daemon = True
        print_thread.start()
        self.run()

    def run(self):
        self.frameDt = 0
        self.running = True
        while self.running:
            self.t = time.time() - self.t0

            self.__handleInput()
            self.__resetDisplay()
            self.__calculateCursor()
            self.__drawDrawList()
            self.__playAnimations()
            if self.panning:
                self.__handlePanning(self.mouseButtonDown,self.dragging)
            self.__performUpdateList()
            self.__handleInteractivity()

            self.display.blit(self.surface,(0,0))
            self.__drawCursor()

            pygame.display.update()
            self.frameDt = self.clock.tick(60) / 1000
            self.mouseButtonDown = False #because this should only be True for a single frame
            self.__debug()

        pygame.quit()

    def __debug(self):
        pass
