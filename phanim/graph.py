from phanim import *
import numpy as np
import itertools

class Graph(Group):
    def __init__(self,vertices,edges,position=[0,0],k=3,initalPositions = False,edgeWidth=2,setup = True,nodeRadius=0.15):

        self.initalPositions = initalPositions
        self.nodeRadius = 0.15
        self.position = position
        self.rotation = 0
        self.vertices = vertices
        self.edges = edges
        self.k = k/np.sqrt(vertices)

        self.locked = False

        self.edgeWidth = edgeWidth
        self.interacting = False
        self.createNodesAndLines()
        self.setPositions()
        self.setNodesAndLines()
        if setup:
            self.setup()
    
    def setup(self):
        for i in range(100):
            self.update(1/30)
        pass


    def setPositions(self):
        self.velocities = []

        if self.initalPositions != False:
            self.positions = self.initalPositions
        else:
            self.positions = []

            for i in range(self.vertices):
                self.positions.append([
                    (np.random.random()-0.5)*4,
                    (np.random.random()-0.5)*3,
                ])
                self.velocities.append([0,0])
    
    def createNodesAndLines(self):
        self.nodes = []
        self.lineList = []

        for i in range(self.vertices):
            self.nodes.append(Node(radius=self.nodeRadius))

        for i in range(len(self.edges)):
            self.lineList.append(Line(color=randomColor(range=[200,255]),lineWidth=self.edgeWidth))
    
    def setNodesAndLines(self):
        self.groupObjects = []

        for i in range(self.vertices):
            self.nodes[i].setPosition(vadd(self.positions[i],self.position))

        for i,edge in enumerate(self.edges):
            self.lineList[i].setEnds(vadd(self.positions[edge[0]],self.position),vadd(self.position,self.positions[edge[1]]))

        for line in self.lineList:
            self.groupObjects.append(line)
        for node in self.nodes:
            self.groupObjects.append(node)
    
    def update(self,dt):
        for i in range(len(self.positions)):
            attractiveForce = [0,0]
            repulsiveForce = [0,0]

            for j in range(len(self.positions)):
                if j!=i:
                    distance = magnitude(diff(self.positions[i],self.positions[j]))
                    direction = normalize(diff(self.positions[i],self.positions[j]))
                    repulsiveForce = vadd(repulsiveForce,direction*self.k**2/distance)

            for edge in self.edges:
                if edge[0] == i:
                    distance = magnitude(diff(self.positions[i],self.positions[edge[1]]))
                    direction = normalize(diff(self.positions[i],self.positions[edge[1]]))
                if edge[1] == i:
                    distance = magSquared(diff(self.positions[i],self.positions[edge[0]]))
                    direction = normalize(diff(self.positions[i],self.positions[edge[0]]))
                if edge[1] == i or edge[0] == i:
                    attractiveForce = vadd(attractiveForce,-direction*distance/self.k)

            centerForce = -normalize(self.positions[i])*magnitude(self.positions[i])/2

            force = vadd(attractiveForce,repulsiveForce,centerForce)

            randomizeSize = 0.1
            force = vadd(force,[(np.random.random()-0.5)*randomizeSize,(np.random.random()-0.5)*randomizeSize])

            self.positions[i] = vadd(self.positions[i], force*dt)

        avaragePosition = [0,0]

        if self.locked:
            for position in self.positions:
                avaragePosition = vadd(avaragePosition,np.array(position)/len(self.positions))

            for index,position in enumerate(self.positions):
                self.positions[index] = diff(position,avaragePosition)
                
        if not self.interacting:
            self.positions = rotateToAlign(self.positions,self.rotation)

        self.setNodesAndLines()

    def setPosition(self,target):
        self.position=target
        self.setNodesAndLines()

    def updateInteractivity(self,screen):
        self.interacting = False
        for index,phobject in enumerate(self.nodes):
            if phobject in screen.selectedObjects:
                phobject.setColor((100,100,100))
                if screen.dragging:
                    self.positions[index] = vadd(screen.camera.position,screen.mousePos)
                    self.interacting=True
                    self.rotation = calculateRotation(diff(self.positions[1],self.positions[0]))
            else:
                phobject.setColor((0,0,0))
        self.setNodesAndLines()

class RandomGraph(Graph):
    def __init__(self,vertices,chance=0.5,position=[0,0],k=3,initalPositions = False,edgeWidth=2,setup = True,nodeRadius=0.15):
        edges = []
        for edge in itertools.combinations(range(vertices),2):
            if np.random.random() < chance:
                edges.append(list(edge))
        super().__init__(vertices,edges,position=position,k=k,initalPositions=initalPositions,edgeWidth=edgeWidth,setup=setup,nodeRadius=nodeRadius)

def CompleteGraph(vertices,chance=0.5,position=[0,0],k=4,initalPositions = False,edgeWidth=3,setup = True):
    return RandomGraph(vertices,chance=1,position=position,k=k,initalPositions = initalPositions,edgeWidth=edgeWidth,setup = setup)
    



