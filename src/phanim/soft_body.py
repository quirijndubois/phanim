from phanim.graph import *


class SoftBody(Graph):
    def __init__(self, positions, edges, springConstant=1e3, dampingConstant=3, pressureConstant=500, hull=[], showHull=True, **kwargs):
        vertices = len(positions)
        self.hull = hull
        self.showHull = showHull
        super().__init__(vertices, edges, initalPositions=positions, **kwargs)
        self.polygon = [
            self.positions[i]
            for i in self.hull
        ]

        self.springLengths = self.getEdgeLengths()
        self.velocities = np.array([[0, 0]]*self.vertices, dtype='float64')

        self.springConstant = springConstant
        self.dampingConstant = dampingConstant
        self.pressureConstant = pressureConstant

    def getEdgeLengths(self):
        return [
            magnitude(self.positions[edge[0]]-self.positions[edge[1]]) for edge in self.edges
        ]

    def checkInside(self, point):
        return is_point_in_polygon(point, self.polygon)

    def getArea(self):
        return polygon_area(self.polygon)

    def update(self, screen):

        gravity = np.array([0, -5])

        forces = np.array([[0, 0]]*self.vertices, dtype='float64')

        for i, edge in enumerate(self.edges):

            begin = self.positions[edge[0]]
            end = self.positions[edge[1]]

            l = self.springLengths[i]

            vel = self.velocities[edge[1]] - self.velocities[edge[0]]

            # C, l, dampFactor, begin, end, vel
            force = dampenedSpringForce(
                self.springConstant, l, self.dampingConstant, begin, end, vel)

            forces[edge[0]] = forces[edge[0]]-force
            forces[edge[1]] = forces[edge[1]]+force

        for i in range(self.vertices):
            forces[i] += gravity

        if hasattr(self, "interactiveForces"):
            for i in range(self.vertices):
                forces[i] += self.interactiveForces[i]

        area = self.getArea()

        if area < 0.0001:
            area = 0.0001

        for i in range(len(self.hull)):

            nextIndex = (i+1) % len(self.hull)

            begin = self.positions[self.hull[i]]
            end = self.positions[self.hull[nextIndex]]

            normal = calculateNormal(end-begin)

            s = magnitude(begin-end)
            forceSize = self.pressureConstant*s/area

            forces[self.hull[i]] += forceSize*normal
            forces[self.hull[nextIndex]] += forceSize*normal

        self.velocities += forces * screen.dt
        self.positions += self.velocities * screen.dt

        self.setNodesAndLines()

        self.polygon = [
            self.positions[i]
            for i in self.hull
        ]

    def setNodesAndLines(self):
        self.groupObjects = []

        for i in range(self.vertices):
            self.nodes[i].setPosition(self.positions[i]+self.position)

        for i, edge in enumerate(self.edges):
            self.lineList[i].setEnds(
                self.positions[edge[0]]+self.position, self.position+self.positions[edge[1]])

        for line in self.lineList:
            self.groupObjects.append(line)

        if len(self.hull) > 0 and self.showHull:
            self.groupObjects.append(
                Polygon(
                    [
                        self.positions[i]
                        for i in self.hull
                    ],
                )
            )

        for node in self.nodes:
            self.groupObjects.append(node)

    def updateInteractivity(self, screen):
        self.updateForceInteractivity(screen)
