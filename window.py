import moderngl

def wError(input):
    wErrorString = "WINDOW: "
    print(wErrorString+input)
    
class Window():
    def __init__(self):
        self.ctx = moderngl.create_context(standalone=True)
        
    def createWindow(self):
        wError("WARING: Window opening is still being worked on and will not work properly! (if at all)")
        
    def test(self,n=1):
        for i in range(n):
            s = "Test succesful!"
            if n > 1:
                wError(f"{s} ({i+1})")
            else:
                wError(s)

    
