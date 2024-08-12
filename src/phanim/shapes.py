from .curve import *

class Quadrilateral(Curve):

    def __init__(self,position=[0,0],strokeWidth=0.05,color=(255,255,255),corners=[[1,1],[-1,1],[-1,-1],[1,-1]],resolution=100):
        super().__init__(position,strokeWidth,color)
        self.corners = np.array(corners)
        self.resolution = resolution
        self.setQuadrilateral()

    def setQuadrilateral(self):
        points = []
        for i in range(4):
            for t in np.linspace(0,1,int(self.resolution/4)):
                if i == 3:
                    pos = interp(self.corners[i],self.corners[0], t)
                else:
                    pos = interp(self.corners[i],self.corners[i+1], t)
                points.append(np.array(pos))

        self.setPoints(points)

class Rectangle(Quadrilateral):
    def __init__(self,position=[0,0],strokeWidth=0.05,color=(255,255,255),width=2,height=2,resolution=100):
        super().__init__(position,strokeWidth,color)
        self.width = width
        self.height = height
        self.setRectange()
    def setRectange(self):
        a = [+self.width/2,+self.height/2]
        b = [-self.width/2,+self.height/2]
        c = [-self.width/2,-self.height/2]
        d = [+self.width/2,-self.height/2]
        self.corners = np.array([a,b,c,d])
        self.setQuadrilateral()


class Circle(Curve):
    def __init__(self,position=[0,0],strokeWidth=0.05,color=(255,255,255),radius=1,resolution=100):
        super().__init__(position,strokeWidth,color)
        self.setCircle(radius, resolution)
        self.radius = radius
    
    def setCircle(self,radius,resolution):
        points = []
        for t in np.linspace(0,2*np.pi,resolution,resolution):
            points.append([
                radius*np.cos(t),
                radius*np.sin(t)
            ])
        self.setPoints(points)

class Triangle(Curve):
    def __init__(self,position=[0,0],strokeWidth=0.05,color=(255,255,255),corners=[[1,-1],[0,1],[-1,-1]],resolution=100):
        super().__init__(position,strokeWidth,color)
        self.corners = corners
        self.resolution = resolution
        self.setTriangle()
    
    def setTriangle(self):
        rest = self.resolution%3
        points = []
        for t in np.linspace(0,1,int(self.resolution/3)+rest):
            points.append(interp(self.corners[0],self.corners[1], t))
        for t in np.linspace(0,1,int(self.resolution/3)):
            points.append(interp(self.corners[1],self.corners[2], t))
        for t in np.linspace(0,1,int(self.resolution/3)):
            points.append(interp(self.corners[2],self.corners[0], t))
        self.setPoints(points)