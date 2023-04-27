from .curve import *

class Quadrilateral(Curve):

    def __init__(self,position=[0,0],strokeWidth=0.05,color=(255,255,255),corners=[[1,1],[-1,1],[-1,-1],[1,-1]],resolution=100):
        super().__init__(position,strokeWidth,color)
        self.corners = corners
        self.resolution = resolution
        self.setQuadrilateral()

    def setQuadrilateral(self):
        points = []
        for i in range(4):
            for t in np.linspace(0,1,int(self.resolution/4)):
                if i == 3:
                    pos = interp2d(self.corners[i],self.corners[0], t)
                else:
                    pos = interp2d(self.corners[i],self.corners[i+1], t)
                points.append(np.array(pos)+self.position)

        self.setPoints(points)

class Rectangle(Quadrilateral):
    def __init__(self,position=[0,0],strokeWidth=0.05,color=(255,255,255),width=2,height=2,resolution=100):
        super().__init__(position,strokeWidth,color)
        self.width = width
        self.height = height
        self.setRectange()
    def setRectange(self):
        a = [self.position[0]+self.width/2,self.position[1]+self.height/2]
        b = [self.position[0]-self.width/2,self.position[1]+self.height/2]
        c = [self.position[0]-self.width/2,self.position[1]-self.height/2]
        d = [self.position[0]+self.width/2,self.position[1]-self.height/2]
        self.corners = [a,b,c,d]
        self.setQuadrilateral()


class Circle(Curve):
    def __init__(self,position=[0,0],strokeWidth=0.05,color=(255,255,255),radius=1,resolution=100):
        super().__init__(position,strokeWidth,color)
        self.setCircle(radius, resolution)
    
    def setCircle(self,radius,resolution):
        points = []
        for t in np.linspace(0,2*np.pi,resolution,resolution):
            points.append([
                radius*np.cos(t),
                radius*np.sin(t)
            ])
        self.setPoints(points)