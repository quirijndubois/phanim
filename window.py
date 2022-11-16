import moderngl
import moderngl_window as mglw

import phanim.info as i


def wError(input):
    wErrorString = "WINDOW: "
    print(wErrorString+input)


class WindowContext(mglw.WindowConfig):
    gl_version = (3, 3)
    window_size = (500, 500)
    width, height = window_size[0],window_size[1]
    aspect_ratio = 16 / 9
    title = "My Config"
    resizable = True
    samples = 8
    updaters = []
    mouseX = 0
    mouseY = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def render(self, time, frametime):
        self.ctx.clear(*self.background)
        self.time = time
        self.frametime = frametime
        for updater in self.updaters:
            updater(self)
        
    def setBackground(self,background):
        self.background = background
    
    def mouse_position_event(self, x, y, dx, dy):
        self.mouseX = x
        self.mouseY = y


class Window():
    def __init__(self):
        self.ctx = moderngl.create_context(standalone=True)
        self.ctx = WindowContext
        
    def openWindow(self):
        wError("WARING: Window opening is still being worked on and will not work properly! (if at all)")
        self.ctx.run()
    
    def setBackground(self,background):
        self.ctx.background = background

    def setResolution(self,resolution):
        self.ctx.window_size = resolution

    def getMouse(self):
        return self.ctx.mouseX, self.ctx.mouseY

    def addUpdater(self,function):
        self.ctx.updaters.append(function)

    def test(self,n=1):
        for i in range(n):
            s = "Test succesful!"
            if n > 1:
                wError(f"{s} ({i+1})")
            else:
                wError(s)

    
