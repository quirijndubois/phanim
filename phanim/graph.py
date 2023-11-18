from phanim import *
import numpy as np
import itertools

class Graph(Group):
    def __init__(self,vertices,edges,position=[0,0],k=4,initalPositions = False,edgeWidth=3):

        self.initalPositions = initalPositions

        self.position = position
        self.vertices = vertices
        self.edges = edges
        self.k = k/np.sqrt(vertices)

        self.edgeWidth = edgeWidth

        self.createNodesAndLines()
        self.setPositions()
        self.setNodesAndLines()
        self.setup()
    
    def setup(self):
        for i in range(1000):
            self.update(1/60)
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
            self.nodes.append(Node())

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
        for position in self.positions:
            avaragePosition = vadd(avaragePosition,np.array(position)/len(self.positions))
        


        for index,position in enumerate(self.positions):
            self.positions[index] = diff(position,avaragePosition)
        
        self.positions = rotateToAlign(self.positions)

        self.setNodesAndLines()

    def setPosition(self,target):
        self.position=target
        self.setNodesAndLines()

class CompleteGraph(Graph):
    def __init__(self,vertices,position=[0,0],k=4,initalPositions = False,edgeWidth=3):
        edges = []
        for edge in itertools.combinations(range(vertices),2):
            edges.append(list(edge))
        self.chance = 0.5

        self.initalPositions = initalPositions

        self.position = position
        self.vertices = vertices
        self.edges = edges
        self.k = k/np.sqrt(vertices)

        self.edgeWidth = edgeWidth

        self.createNodesAndLines()
        self.setPositions()
        self.setNodesAndLines()
        self.setup()
            

class RandomGraph(Graph):
    def __init__(self,vertices,position=[0,0],k=4,chance=0.5,initalPositions = False,edgeWidth=3):
        edges = []
        for edge in itertools.combinations(range(vertices),2):
            if np.random.random() < chance:
                edges.append(list(edge))
        self.chance = 0.5

        self.initalPositions = initalPositions

        self.position = position
        self.vertices = vertices
        self.edges = edges
        self.k = k/np.sqrt(vertices)

        self.edgeWidth = edgeWidth

        self.createNodesAndLines()
        self.setPositions()
        self.setNodesAndLines()
        self.setup()


    



