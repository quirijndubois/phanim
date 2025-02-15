from phanim import *
import random

# NOT FINISHED!


class Bead(Group):

    def __init__(self, pos, speed, angle):
        self.position = np.array(pos)
        self.speed = speed
        self.angle = angle
        self.groupObjects = [Arrow(color=white), Node(
            self.position, radius=0.08)]

        dir = np.array([np.cos(self.angle), np.sin(self.angle)])
        self.groupObjects[0].setDirection(self.position, dir, .3)

        self.closeBeads = []

    def update(self, screen):
        self.vel = np.array(
            [np.cos(self.angle), np.sin(self.angle)]) * self.speed
        self.position += self.speed * self.vel * screen.dt
        if self.position[0] < screen.camera.bounds[0][0]:
            self.position[0] = screen.camera.bounds[0][1]
        elif self.position[0] > screen.camera.bounds[0][1]:
            self.position[0] = screen.camera.bounds[0][0]

        if self.position[1] < screen.camera.bounds[1][0]:
            self.position[1] = screen.camera.bounds[1][1]
        elif self.position[1] > screen.camera.bounds[1][1]:
            self.position[1] = screen.camera.bounds[1][0]

        self.groupObjects[0].setDirection(self.position, self.vel, .3)
        self.groupObjects[1].setPosition(self.position)


class Beads(Group):

    def __init__(self, n, bounds):
        self.position = np.array([0, 0])
        self.groupObjects = []
        self.setRotation(0)
        for i in range(n):
            self.groupObjects.append(Bead(
                [random.uniform(*bounds[0]), random.uniform(*bounds[1])], 1, random.uniform(0, 2*np.pi)))

    def update(self, screen):
        for i in range(len(self.groupObjects)):

            self.groupObjects[i].closeBeads = []
            for j in range(len(self.groupObjects)):
                if i == j:
                    continue
                if magSquared(self.groupObjects[i].position - self.groupObjects[j].position) < 1:
                    self.groupObjects[i].closeBeads.append(
                        self.groupObjects[j])

            self.groupObjects[i].update(screen)


s = Screen(zooming=False)

beads = Beads(50, s.camera.bounds)

s.addUpdater(beads.update)

s.play(Create(beads))

s.run()
