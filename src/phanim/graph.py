from phanim import *
import itertools
from copy import copy
import numpy as np
from .functions import *


class Graph(Group):
    def __init__(self, vertices, edges, k=3, initalPositions=[], edgeWidth=2, nodeRadius=0.15, **kwargs):
        self.initalPositions = initalPositions
        self.nodeRadius = nodeRadius
        self.vertices = vertices
        self.edges = edges
        self.k = k/np.sqrt(vertices)

        self.locked = False

        self.edgeWidth = edgeWidth
        self.interacting = False

        self.createNodesAndLines()
        self.setPositions()

        super().__init__(**kwargs)

    def join(self, graph):
        for edge in graph.edges:
            self.edges.append([edge[0]+self.vertices, edge[1]+self.vertices])
        self.vertices += graph.vertices
        self.positions += graph.positions
        self.createNodesAndLines()
        self.setNodesAndLines()

    def setPositions(self):
        self.velocities = []

        if len(self.initalPositions) != 0:

            self.positions = np.array(
                copy(self.initalPositions), dtype='float64')

        else:
            self.positions = []

            for i in range(self.vertices):
                self.positions.append([
                    (np.random.random()-0.5)*4,
                    (np.random.random()-0.5)*3,
                ])
                self.velocities.append([0, 0])
        self.positions = np.array(self.positions)

    def createNodesAndLines(self):
        self.nodes = []
        self.lineList = []

        for i in range(self.vertices):
            self.nodes.append(Node(radius=self.nodeRadius))

        for i in range(len(self.edges)):
            if len(self.edges[i]) > 2:
                self.lineList.append(DottedLine(color=randomColor(
                    range=[200, 255]), lineWidth=self.edgeWidth))
            else:
                self.lineList.append(Line(color=randomColor(
                    range=[200, 255]), lineWidth=self.edgeWidth))

    def setNodesAndLines(self):
        self.groupObjects = []

        for i in range(self.vertices):
            self.nodes[i].setPosition(self.positions[i]+self.position)

        for i, edge in enumerate(self.edges):
            self.lineList[i].setEnds(
                self.positions[edge[0]]+self.position, self.position+self.positions[edge[1]])

        for line in self.lineList:
            self.groupObjects.append(line)
        for node in self.nodes:
            self.groupObjects.append(node)

    def update(self, screen):
        dt = screen.dt
        for i in range(len(self.positions)):
            attractiveForce = [0, 0]
            repulsiveForce = [0, 0]

            for j in range(len(self.positions)):
                if j != i:
                    distance = magnitude(self.positions[i]-self.positions[j])
                    direction = normalize(self.positions[i]-self.positions[j])
                    repulsiveForce = repulsiveForce+direction*self.k**2/distance

            for edge in self.edges:
                if edge[0] == i:
                    distance = magnitude(
                        self.positions[i]-self.positions[edge[1]])
                    direction = normalize(
                        self.positions[i]-self.positions[edge[1]])
                if edge[1] == i:
                    distance = magnitude(
                        self.positions[i]-self.positions[edge[0]])
                    direction = normalize(
                        self.positions[i]-self.positions[edge[0]])
                if edge[1] == i or edge[0] == i:
                    attractiveForce = attractiveForce+-direction*distance/self.k

            centerForce = - \
                normalize(self.positions[i])*magnitude(self.positions[i])/2

            force = attractiveForce+repulsiveForce+centerForce

            positionalForce = [0, 0]

            force = force+positionalForce

            self.positions[i] = self.positions[i] + force*dt

        self.setNodesAndLines()

    def setPosition(self, target):
        self.position = target
        self.setNodesAndLines()

    def updateInteractivity(self, screen):
        self.updatePostionInteractivity(screen)

    def updateForceInteractivity(self, screen):
        self.interacting = False
        self.interactiveForces = np.array(
            [[0, 0]]*self.vertices, dtype='float64')
        for index, phobject in enumerate(self.nodes):
            if phobject in screen.selectedObjects:

                if not self.selected:
                    self.offset = self.positions[index] - \
                        screen.GlobalCursorPosition

                phobject.setColor((100, 100, 100))

                if screen.dragging:
                    self.selected = True
                    self.interacting = True

                    screen.draw(
                        Line(begin=screen.GlobalCursorPosition, end=self.positions[index]))

                    force = dampenedSpringForce(
                        500, 0, 40, screen.GlobalCursorPosition, self.positions[index], self.velocities[index])

                    self.velocities[index] *= .9

                    self.interactiveForces[index] = force
                else:
                    self.selected = False

            else:
                phobject.setColor((0, 0, 0))
        self.setNodesAndLines()

    def updatePostionInteractivity(self, screen):

        self.interacting = False
        for index, phobject in enumerate(self.nodes):
            if phobject in screen.selectedObjects:

                if not self.selected:
                    self.offset = self.positions[index] - \
                        screen.GlobalCursorPosition

                phobject.setColor((100, 100, 100))

                if screen.dragging:
                    self.selected = True
                    self.positions[index] = screen.GlobalCursorPosition + self.offset
                    self.interacting = True

                else:
                    self.selected = False

            else:
                phobject.setColor((0, 0, 0))
        self.setNodesAndLines()


class RandomGraph(Graph):
    def __init__(self, vertices, chance=0.5, position=[0, 0], k=3, initalPositions=[], edgeWidth=2, nodeRadius=0.15):
        edges = []
        for edge in itertools.combinations(range(vertices), 2):
            if np.random.random() < chance:
                edges.append(list(edge))
        super().__init__(vertices, edges, position=position, k=k, initalPositions=initalPositions,
                         edgeWidth=edgeWidth, nodeRadius=nodeRadius)


def CompleteGraph(vertices, chance=0.5, position=[0, 0], k=4, initalPositions=[], edgeWidth=3):
    return RandomGraph(vertices, chance=1, position=position, k=k, initalPositions=initalPositions, edgeWidth=edgeWidth)
