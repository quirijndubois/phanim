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
        record (bool): Whether the screen is being recorded.,
        recording_output (str): The output file for the screen recording.
        recording_fps (int): The FPS for the screen recording.
        zoomSpeed (float): The speed at which the camera zooms.
        zoomSmoothingConstant (float): The smoothing constant for the camera zoom.
    """

    def __init__(
            self,
            resolution=None,
            zoom=6,
            fullscreen=True,
            background=(10, 15, 20),
            fontSize=0.5,
            panning=True,
            zooming=True,
            renderer="pygame",
            grid=True,
            gridMargin=[60, 60],
            gridResolution=15,
            gridBrightness=150,
            expand_grid=True,
            record=False,
            recording_output="recording.mp4",
            recording_fps=60,
            zoomSpeed=1.5,
            zoomSmoothingConstant=0.4,
    ):

        if renderer == "pygame":
            self.renderer = PygameRenderer(resolution, fontSize, fullscreen, record=record,
                                           recording_output=recording_output, recording_fps=recording_fps)
        elif renderer == "moderngl":
            self.renderer = ModernGLRenderer(resolution, fontSize, fullscreen)
        else:
            raise "Render engine not found!"
        self.rendererName = renderer

        self.resolution = self.renderer.resolution

        self.camera = Camera(zoom, self.resolution)
        self.static_camera = Camera(zoom, self.resolution)

        self.fontSize = int(fontSize*self.camera.pixelsPerUnit)

        # Setting static settings
        self.record = record
        self.panning = panning
        self.zooming = zooming
        self.gridMargin = gridMargin
        self.background = background
        self.mouseThightness = 0.3
        self.zoomSpeed = zoomSpeed
        self.zoomSmoothingConstant = zoomSmoothingConstant

        # preparing lists
        self.updaterList = []
        self.mouseClickUpdaterList = []
        self.mouseDragUpdaterList = []
        self.mouseDownUpdaterList = []
        self.interativityList = []
        self.animationQueue = []
        self.drawList = []
        self.selectedObjects = []

        # presetting dynamic variables
        self.dragging = False
        self.mouseButtonDown = False
        self.t0 = time.time()
        self.scroll = [0, 0]
        self.lastScroll = [0, 0]
        self.grid = grid
        self.gridResolution = gridResolution
        self.gridBrightness = gridBrightness

        self.frameDt = 1/recording_fps
        self.frameRate = recording_fps

        if expand_grid and grid:
            self.expandGrid()

    def addUpdater(self, someFunction, substeps=1):
        """
        This method is called to add an updater. I.E. a function that updates every frame.

        Args:
            someFunction (function): The function to be called when the mouse button is released.
        """
        self.updaterList.append([someFunction, substeps])

    def addMouseClickUpdater(self, someFunction):
        """
        Similar to addUpdater, but only called when the mouse is released.

        Args:
            someFunction (function): The function to be called when the mouse button is released.
        """
        self.mouseClickUpdaterList.append(someFunction)

    def addMouseDownUpdater(self, someFunction):
        """
        Similar to addUpdater, but only called when the mouse button is pressed down.

        Args:
            someFunction (function): The function to be called when the mouse button is pressed down.
        """
        self.mouseDownUpdaterList.append(someFunction)

    def addMouseDragUpdater(self, someFunction):
        """
        Similar to addUpdater, but only called when the mouse button is being dragged.

        Args:
            someFunction (function): The function to be called when the mouse button is being dragged.
        """
        self.mouseDragUpdaterList.append(someFunction)

    def __handlePanning(self, mouseDown, dragging):
        if len(self.selectedObjects) > 0:
            dragging = False
        if mouseDown:
            self.panBeginCameraPosition = self.camera.position
            self.panBeginMousePos = self.LocalCursorPosition
        if dragging:
            self.camera.setPosition(
                (self.panBeginMousePos-self.LocalCursorPosition)+(self.panBeginCameraPosition))

        if self.zooming:
            scroll = self.scroll
            scroll[0] /= 30
            scroll[1] /= 30
            self.camera.setZoom(self.camera.targetZoom -
                                self.camera.targetZoom*scroll[1]*self.zoomSpeed)
        self.camera.update(self.zoomSmoothingConstant)

    def drawLines(self, lines, width, position,rotationMatrix, static=False):
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

        if static:
            cam = self.static_camera
        else:
            cam = self.camera

        for line in lines:
            start = cam.coords2screen(line[0]@rotationMatrix + position)
            stop = cam.coords2screen(line[1]@rotationMatrix + position)

            pixelWidth = int(width/cam.zoom*20)
            if pixelWidth < 1:
                pixelWidth = 1.5

            if len(line) == 3:
                color = line[2]
            else:
                color = (255, 255, 255)
            self.renderer.drawLine(color, start, stop, pixelWidth)

    def __drawCircles(self, circles, position, rotationMatrix, static=False):
        if static:
            cam = self.static_camera
        else:
            cam = self.camera

        for circle in circles:
            pos = cam.coords2screen(circle[1]@rotationMatrix+position) 
            self.renderer.drawCircle(
                circle[2], pos, circle[0]*cam.pixelsPerUnit)

    def __drawPolygons(self, polygons, color, position,rotationMatrix, static=False):
        if static:
            cam = self.static_camera
        else:
            cam = self.camera

        for polygon in polygons:
            points = []
            for point in polygon:
                points.append(cam.coords2screen(point@rotationMatrix+position))
            self.renderer.drawPolygon(color, points)

    def __drawTexts(self, texts, position, static=False):
        if static:
            cam = self.static_camera
        else:
            cam = self.camera

        for text in texts:
            position = cam.coords2screen(position)
            color = text[2]
            size = text[1]
            text = text[0]
            size = int(size/cam.zoom*20)

            # We cap size for performance reasons
            if size < 1000:
                self.renderer.drawText(color, text, position, size)

    def __drawPhobject(self, phobject, static=False):

        if hasattr(phobject, "polygons"):
            self.__drawPolygons(phobject.polygons,
                                phobject.color, phobject.position, phobject.rotationMatrix, static=static)
        if hasattr(phobject, 'circles'):
            self.__drawCircles(
                phobject.circles, phobject.position, phobject.rotationMatrix, static=static)
        if hasattr(phobject, 'lines'):
            self.drawLines(phobject.lines, phobject.lineWidth,
                           phobject.position, phobject.rotationMatrix, static=static)
        if hasattr(phobject, "texts"):
            self.__drawTexts(phobject.texts, phobject.position, static=static)

    def draw(self, *args, static=False):
        """
        Draws the given phobjects or groups of phobjects on the screen.

        Parameters:
            *args: variable number of phobjects or groups of phobjects to be drawn

        Returns:
            None
        """
        for arg in args:

            if len(args) > 1:
                static = False
            if hasattr(arg, "static"):
                if arg.static:
                    static = True

            if hasattr(arg, "groupObjects"):
                for phobject in arg.groupObjects:
                    self.draw(phobject, static=static)
            else:
                self.__drawPhobject(arg, static=static)

    def __drawGrid(self, spacing, color=(255, 255, 255), margin=[0, 0]):
        group = Group()
        boundX = self.camera.bounds[0] + \
            np.array([margin[0], -margin[0]])/self.camera.pixelsPerUnit
        boundY = self.camera.bounds[1] + \
            np.array([margin[1], -margin[1]])/self.camera.pixelsPerUnit

        amountX = int(np.ceil((boundX[1]-boundX[0])/spacing))
        amountY = int(np.ceil((boundY[1]-boundY[0])/spacing))

        for i in range(amountX):
            start = [np.ceil(boundX[0]/spacing)*spacing + i*spacing, boundY[0]]
            stop = [np.ceil(boundX[0]/spacing)*spacing+i*spacing, boundY[1]]

            if margin[0] > 0:
                if start[0] > boundX[1]:
                    start[0] = boundX[1]
                    stop[0] = boundX[1]

            group.add(Line(
                begin=start,
                end=stop,
                lineWidth=0,
                color=color
            )
            )
        for i in range(amountY):
            start = [boundX[0], np.ceil(boundY[0]/spacing)*spacing+i*spacing]
            stop = [boundX[1], np.ceil(boundY[0]/spacing)*spacing+i*spacing]

            if margin[1] > 0:
                if start[1] > boundY[1]:
                    start[1] = boundY[1]
                    stop[1] = boundY[1]

            group.add(Line(
                begin=start,
                end=stop,
                lineWidth=0,
                color=color
            )
            )
        if margin[0] > 0:
            group.add(
                Line(
                    begin=[boundX[0], boundY[1]],
                    end=[boundX[0], boundY[0]],
                    lineWidth=0,
                    color=color
                ),
                Line(
                    begin=[boundX[1], boundY[0]],
                    end=[boundX[1], boundY[1]],
                    lineWidth=0,
                    color=color
                ),
            )
        if margin[1] > 0:
            group.add(
                Line(
                    begin=[boundX[0], boundY[0]],
                    end=[boundX[1], boundY[0]],
                    lineWidth=0,
                    color=color
                ),
                Line(
                    begin=[boundX[1], boundY[1]],
                    end=[boundX[0], boundY[1]],
                    lineWidth=0,
                    color=color
                ),
            )

        self.draw(group)

    def __createGrid(self):
        width = self.camera.bounds[0][1]-self.camera.bounds[0][0]
        closestPower, distance = round_to_power_of_2(width/self.gridResolution)
        if self.rendererName == "pygame":
            self.__drawGrid(
                closestPower/4,
                color=(255, 255, 255, interp(
                    0, self.gridBrightness/3, distance)),
                margin=self.gridMargin
            )
            self.__drawGrid(
                closestPower/2,
                color=(255, 255, 255, interp(
                    self.gridBrightness/3, self.gridBrightness, distance)),
                margin=self.gridMargin
            )
            self.__drawGrid(
                closestPower,
                color=(255, 255, 255, self.gridBrightness),
                margin=self.gridMargin
            )

        elif self.rendererName == "moderngl":
            color1 = interp(0, self.gridBrightness/3, distance)
            color2 = interp(self.gridBrightness/3,
                            self.gridBrightness, distance)
            color3 = self.gridBrightness
            self.__drawGrid(closestPower/4, color=(color1,
                            color1, color1), margin=self.gridMargin)
            self.__drawGrid(closestPower/2, color=(color2,
                            color2, color2), margin=self.gridMargin)
            self.__drawGrid(closestPower, color=(
                color3, color3, color3), margin=self.gridMargin)

    def makeInteractive(self, *args):
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

                static = False
                if hasattr(phobject, "static"):
                    if phobject.static:
                        static = True

                if static:
                    mouse = self.StaticCursorPosition
                else:
                    mouse = self.GlobalCursorPosition

                if hasattr(phobject, "radius"):
                    if magnitude(phobject.position-mouse) < phobject.radius:
                        self.selectedObjects.append(phobject)
                elif hasattr(phobject, "checkSelection"):
                    if phobject.checkSelection(self):
                        self.selectedObjects.append(phobject)
                elif hasattr(phobject, "groupObjects"):
                    for phobject2 in phobject.groupObjects:
                        if hasattr(phobject2, "radius"):
                            if magnitude(phobject2.position-mouse) < phobject2.radius:
                                self.selectedObjects.append(phobject2)

        for phobject in self.interativityList:
            if hasattr(phobject, "updateInteractivity"):
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
                    self.scroll = [event.x, event.y]

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
        self.LocalCursorPosition = self.camera.screen2coords(pos)
        self.GlobalCursorPosition = self.LocalCursorPosition+self.camera.position
        self.StaticCursorPosition = self.LocalCursorPosition / \
            self.camera.zoom * self.static_camera.zoom

    def __performUpdateList(self):
        if self.t > .1:
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
        self.renderer.drawCircle(color, center, radius, segments=10)

    def setGridMargin(self, *args):
        if len(args) == 1:
            self.gridMargin[0] = args[0]
            self.gridMargin[1] = args[0]
        elif len(args) == 2:
            self.gridMargin[0] = args[0]
            self.gridMargin[1] = args[1]
        else:
            raise NotImplementedError

    def play(self, *args):
        """
        Adds the given arguments to the animation queue, which is used to schedule animations to be played on the screen.

        Parameters:
            *args (Any): The arguments to be added to the animation queue. These can be any type of object that can be passed as arguments to the draw method.

        Returns:
            None
        """

        self.animationQueue.append(list(args))

    def wait(self, duration):
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
            for index, animation in enumerate(self.animationQueue[0]):

                if animation.mode == "wrapper":
                    animation.currentFrame += 1
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

    def __drawAnimation(self, animation):
        if animation.currentFrame == 0:
            if hasattr(animation, "object"):
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

    def __drawWrapperAnimation(self, animation):
        for index, wrappedAnimation in enumerate(animation.animations):
            if wrappedAnimation.currentFrame == 0:
                if hasattr(wrappedAnimation, "object"):
                    wrappedAnimation.oldPhobject = copy(
                        wrappedAnimation.object)
            if wrappedAnimation.mode == "add":
                self.draw(wrappedAnimation)

    def add(self, *args):
        """
        Adds a phobject to the draw list.

        Args:
            phobject (any): The phobject to be added to the draw list.

        Returns:
            None
        """
        for phobject in args:
            self.drawList.append(phobject)

    def remove(self, phobject):
        """
        Removes a phobject from the draw list.

        Args:
            phobject (any): The phobject to be removed from the draw list.

        Returns:
            None
        """
        self.drawList.remove(phobject)

    def expandGrid(self):
        self.wait(30)
        target = copy(self.gridMargin)
        self.setGridMargin(self.resolution[0]/2, self.resolution[1]/2)
        self.play(AnimateValue(
            lambda value: self.setGridMargin(value, self.gridMargin[1]),
            [self.resolution[0]/2, target[0]],
            duration=30
        ))
        self.play(AnimateValue(
            lambda value: self.setGridMargin(target[0], value),
            [self.resolution[1]/2, target[1]],
            duration=30
        ))

    def __drawDrawList(self):
        self.draw(*self.drawList)

    def run_interactive(self, globals):
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
                self.__handlePanning(self.mouseButtonDown, self.dragging)
            self.__handleInteractivity()
            self.__performUpdateList()

            self.__drawCursor()
            self.renderer.update(self.background)

            if not self.record:
                self.frameDt = self.renderer.getFrameDeltaTime()
                self.frameRate = 1 / self.frameDt

            self.mouseButtonDown = False  # because this should only be True for a single frame
            self.__debug()

        self.renderer.quit()

    def __debug(self):
        pass
