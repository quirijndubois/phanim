from . functions import *
from . camera import *
from . animate import *
from . renderer import *
import time
from copy import copy
from copy import deepcopy
import threading

class Screen():
    
    """
    The Screen class is the backbone of the Phanim library and represents the windows where are animation are played.

    Args:
        resolution (tuple): The resolution of the screen in pixels.
        zoom (float): The initial zoom level of the camera.
        fullscreen (bool): Whether the screen should be displayed in fullscreen mode.
        background (tuple): The background color of the screen in RGB format.
        fontSize (float): The font size for text rendering.
        panning (bool): Whether the camera should allow panning.
        renderer (str): The rendering engine to use (e.g. "pygame", "moderngl").
        grid (bool): Whether to display a grid on the screen.
        gridResolution (int): The resolution of the grid.
        gridBrightness (int): The brightness of the grid lines.

    Attributes:
        resolution (tuple): The resolution of the screen in pixels.
        camera (Camera): The camera object managing the screen's view.
        fontSize (int): The font size for text rendering in pixels.
        renderer (Renderer): The rendering engine instance.
        rendererName (str): The name of the rendering engine.
        record (bool): Whether the screen is being recorded.
        recording_output (str): The output file for the screen recording.
        recording_fps (int): The FPS for the screen recording.
    """

    def __init__(self,resolution=None,zoom = 6,fullscreen=True,background=(10,15,20),fontSize=0.5,panning=True,renderer="pygame",grid=True,gridResolution=15,gridBrightness=150,record=False,recording_output="recording.mp4",recording_fps=30):
        
        if renderer == "pygame":
            self.renderer = PygameRenderer(resolution,fontSize,fullscreen,record=record,recording_output=recording_output,recording_fps=recording_fps)
        elif renderer == "moderngl":
            self.renderer = ModernGLRenderer(resolution,fontSize,fullscreen)
        else:
            raise "Render engine not found!"
        self.rendererName = renderer

        self.resolution = self.renderer.resolution

        self.camera = Camera(zoom,self.resolution)
        self.fontSize = int(fontSize*self.camera.pixelsPerUnit)

        self.record = record

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
        self.scroll = [0,0]
        self.lastScroll = [0,0]
        self.grid = grid
        self.gridResolution = gridResolution
        self.gridBrightness = gridBrightness

        self.frameDt = 1/recording_fps

    def addUpdater(self,someFunction,substeps=1):
        """
        This method is called to add an updater. I.E. a function that updates every frame.

        Args:
            someFunction (function): The function to be called when the mouse button is released.
        """
        self.updaterList.append([someFunction,substeps])

    def addMouseClickUpdater(self,someFunction):
        """
        Similar to addUpdater, but only called when the mouse is released.

        Args:
            someFunction (function): The function to be called when the mouse button is released.
        """
        self.mouseClickUpdaterList.append(someFunction)
    
    def addMouseDownUpdater(self,someFunction):
        """
        Similar to addUpdater, but only called when the mouse button is pressed down.

        Args:
            someFunction (function): The function to be called when the mouse button is pressed down.
        """
        self.mouseDownUpdaterList.append(someFunction)

    def addMouseDragUpdater(self,someFunction):
        """
        Similar to addUpdater, but only called when the mouse button is being dragged.

        Args:
            someFunction (function): The function to be called when the mouse button is being dragged.
        """
        self.mouseDragUpdaterList.append(someFunction)

    def __handlePanning(self,mouseDown,dragging):
        if len(self.selectedObjects)>0:
            dragging = False
        if mouseDown:
            self.panBeginCameraPosition = self.camera.position
            self.panBeginMousePos = self.mousePos
        if dragging:
            self.camera.setPosition((self.panBeginMousePos-self.mousePos)+(self.panBeginCameraPosition))

        scroll = self.scroll
        scroll[0] /= 30
        scroll[1] /= 30
        self.camera.setZoom(self.camera.zoom - self.camera.zoom*scroll[1])

    def drawLines(self,lines,width,position):
        """
        Draws a list of lines on the screen.

        Args:
            lines (list): A list of lines, where each line is a list of two or three elements.
                The first two elements are the start and stop coordinates of the line.
                The third element is optional and specifies the color of the line.
            width (float): The width of the lines.
            position (list): The position offset of the lines.
        Returns:
            None
        """
        for line in lines:
            start = self.camera.coords2screen(line[0] + position)
            stop = self.camera.coords2screen(line[1] + position)

            pixelWidth = int(width/self.camera.zoom*20)
            if pixelWidth < 1:
                pixelWidth = 1.5

            if len(line) == 3:
                color = line[2]
            else:
                color = (255,255,255)
            self.renderer.drawLine(color,start,stop,pixelWidth)


    def __drawCircles(self,circles,position):
            for circle in circles:
                pos = self.camera.coords2screen(circle[1]+position)
                self.renderer.drawCircle(circle[2], pos, circle[0]*self.camera.pixelsPerUnit)

    def __drawPolygons(self,polygons,color,position):
        for polygon in polygons:
            points = []
            for point in polygon:
                points.append(self.camera.coords2screen(point+position))
            self.renderer.drawPolygon(color, points)

    def __drawText(self,texts,position):
        for text in texts:
            if len(text) > 0:
                img = self.font.render(text[0],True,text[2])
                pos = self.camera.coords2screen(text[1]+position)
                self.display.blit(img,pos)

    def __drawPhobject(self,phobject):
        if hasattr(phobject, 'circles'):
            self.__drawCircles(phobject.circles, phobject.position)
        if hasattr(phobject, 'lines'):
            self.drawLines(phobject.lines, phobject.lineWidth, phobject.position)
        if hasattr(phobject,"polygons"):
            self.__drawPolygons(phobject.polygons,phobject.color, phobject.position)
        if hasattr(phobject, "texts"):
            self.__drawText(phobject.texts, phobject.position)

    def draw(self,*args):
        """
        Draws the given phobjects or groups of phobjects on the screen.
        
        Parameters:
            *args: variable number of phobjects or groups of phobjects to be drawn
        
        Returns:
            None
        """
        for arg in args:
            if hasattr(arg,"groupObjects"):
                for phobject in arg.groupObjects:
                    self.__drawPhobject(phobject)
            else:
                self.__drawPhobject(arg)

    def __drawGrid(self,spacing,color=(255,255,255)):
        group = Group()
        boundX = self.camera.bounds[0]
        boundY = self.camera.bounds[1]
        
        amountX = int(np.ceil((boundX[1]-boundX[0])/spacing))
        amountY = int(np.ceil((boundY[1]-boundY[0])/spacing))

        for i in range(amountX):
            group.add(Line(
                start=[np.ceil(boundX[0]/spacing)*spacing+i*spacing,boundY[0]],
                stop=[np.ceil(boundX[0]/spacing)*spacing+i*spacing,boundY[1]],
                lineWidth=0,
                color=color
                )
            )
        for i in range(amountY):
            group.add(Line(
                start=[boundX[0],np.ceil(boundY[0]/spacing)*spacing+i*spacing],
                stop=[boundX[1],np.ceil(boundY[0]/spacing)*spacing+i*spacing],
                lineWidth=0,
                color=color
                )
            )

        self.draw(group)

    def __createGrid(self):
        width = self.camera.bounds[0][1]-self.camera.bounds[0][0]
        closestPower,distance = round_to_power_of_2(width/self.gridResolution)
        if self.rendererName == "pygame":
            self.__drawGrid(closestPower/4,color=(255,255,255,interp(0,self.gridBrightness/3,distance)))
            self.__drawGrid(closestPower/2,color=(255,255,255,interp(self.gridBrightness/3,self.gridBrightness,distance)))
            self.__drawGrid(closestPower,color=(255,255,255,self.gridBrightness))
        elif self.rendererName == "moderngl":
            color1 = interp(0,self.gridBrightness/3,distance)
            color2 = interp(self.gridBrightness/3,self.gridBrightness,distance)
            color3 = self.gridBrightness
            self.__drawGrid(closestPower/4,color=(color1,color1,color1))
            self.__drawGrid(closestPower/2,color=(color2,color2,color2))
            self.__drawGrid(closestPower,color=(color3,color3,color3))

    def makeInteractive(self,*args):
        """
        Makes the given phobjects interactive. (If the phobject has an ```updateInteractivity``` method)

        Args:
            *args: A variable number of phobjects or lists of phobjects to be made interactive.

        Returns:
            None
        """
        for arg in args:
            if type(arg) is list:
                for phobject in arg:
                    self.interativityList.append(phobject)
            else:
                self.interativityList.append(arg)

    
    def __handleInteractivity(self):
        self.dt = self.frameDt
        if not self.dragging:
            self.selectedObjects = []
            for phobject in self.interativityList:
                if hasattr(phobject,"radius"):
                    if magnitude(phobject.position-(self.mousePos+self.camera.position)) < phobject.radius:
                        self.selectedObjects.append(phobject)
                elif hasattr(phobject,"checkSelection"):
                    if phobject.checkSelection(self):
                        self.selectedObjects.append(phobject)
                elif hasattr(phobject,"groupObjects"):
                    for phobject2 in phobject.groupObjects:
                        if hasattr(phobject2,"radius"):
                            if magnitude(phobject2.position-(self.mousePos+self.camera.position)) < phobject2.radius:
                                self.selectedObjects.append(phobject2)

        for phobject in self.interativityList:
            if hasattr(phobject,"updateInteractivity"):
                phobject.updateInteractivity(self)

    def __handleInput(self):
        if self.rendererName == "pygame":
            self.keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.renderer.isRunning = False
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
        
        if self.rendererName == "moderngl":
            if self.renderer.BUTTONUP:
                self.dragging = False
                for func in self.mouseClickUpdaterList:
                    func(self)
            if self.renderer.BUTTONUP:
                self.dragging = True
                self.mouseButtonDown = True
                for func in self.mouseDownUpdaterList:
                    func(self)
            self.scroll = self.renderer.scroll
            
        if self.dragging:
            for func in self.mouseDragUpdaterList:
                func(self)

    def __resetDisplay(self):
            self.renderer.reset(self.background)

    def __calculateCursor(self):
        pos = self.renderer.getMousePos()
        self.cursorPositionScreen = pos
        self.LocalcursorPosition = self.camera.screen2cords(pos)
        self.GlobalCursorPosition = self.LocalcursorPosition+self.camera.position
        self.mousePos = self.LocalcursorPosition #for version compatibility (should be discontinued)

    def __performUpdateList(self):
        if self.t > 1:
            for func in self.updaterList:
                for i in range(func[1]):
                    self.dt = self.frameDt/func[1]
                    func[0](self)

    def __drawCursor(self):
        radius = 10
        # color = (150, 150, 150, 120)
        color = (150, 150, 150)
        center = self.cursorPositionScreen
        # self.renderer.setCursor(color,center,radius)
        self.renderer.drawCircle(color,center,radius,segments=10)

    def play(self,*args):
        """
        Adds the given arguments to the animation queue, which is used to schedule animations to be played on the screen.

        Parameters:
            *args (Any): The arguments to be added to the animation queue. These can be any type of object that can be passed as arguments to the draw method.

        Returns:
            None
        """

        self.animationQueue.append(list(args))

    def wait(self,duration):
        """
        Pauses the animation for a specified duration.

        Parameters:
            duration (int): The duration of the pause in frames.

        Returns:
            None
        """
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
                    wrappedAnimation.oldPhobject = copy(wrappedAnimation.object)
            if wrappedAnimation.mode == "add":
                self.draw(wrappedAnimation)
        
    def add(self,phobject):
        """
        Adds a phobject to the draw list.

        Args:
            phobject (any): The phobject to be added to the draw list.

        Returns:
            None
        """
        self.drawList.append(phobject)

    def remove(self,phobject):
        """
        Removes a phobject from the draw list.

        Args:
            phobject (any): The phobject to be removed from the draw list.

        Returns:
            None
        """
        self.drawList.remove(phobject)
    
    def __drawDrawList(self):
        self.draw(*self.drawList)

    def run_interactive(self,globals):
        """
        Runs the screen in interactive mode, allowing for IPython input.
        When used, this method replaces Screen.run().

        Args:
            globals (dict): The global namespace to be used in the IPython session.

        Returns:
            None
        """
        from IPython import start_ipython
        
        def thread_loop():
            start_ipython(argv=[], user_ns=globals)

        print_thread = threading.Thread(target=thread_loop)
        print_thread.daemon = True
        print_thread.start()
        self.run()

    def run(self):
        """
        Runs the main loop of the screen, handling user input, rendering, and updating. Necessary for phanim to function.

        Returns:
            None
        """
        while self.renderer.running():
            self.t = time.time() - self.t0

            self.__handleInput()
            self.__calculateCursor()
            if self.grid:
                self.__createGrid()
            self.__drawDrawList()
            self.__playAnimations()
            if self.panning:
                self.__handlePanning(self.mouseButtonDown,self.dragging)
            self.__handleInteractivity()
            self.__performUpdateList()


            self.__drawCursor()
            self.renderer.update(self.background)

            if not self.record:
                self.frameDt = self.renderer.getFrameDeltaTime()
            self.mouseButtonDown = False #because this should only be True for a single frame
            self.__debug()

        self.renderer.quit()

    def __debug(self):
        pass
