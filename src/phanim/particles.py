from .functions import *
from .curve import *
from .phobject import *
from phanim.color import NaturalColorMap
from copy import copy


class ParticlesOld():
    def __init__(self, n=150, lifetime=20, area=[[-5, 5], [-5, 5]], radius=0, colorMap=NaturalColorMap, trails=True, lineWidth=2, speed=100, maxspeed=2e-2, fadingtime=2, distribution="even"):
        self.lifetime = lifetime
        self.area = area
        self.colorMap = colorMap
        self.particles = []
        self.lineWidth = lineWidth
        self.speed = speed
        self.maxspeed = maxspeed
        self.distribution = distribution
        for i in range(n):
            pos = self.distrubute()
            node = Node(pos=pos, radius=radius)
            node.age = np.random.randint(0, self.lifetime)
            if trails:
                node.trail = Trail(length=self.lifetime*fadingtime)
            self.particles.append(node)

    def setVelocity(self, velcityFieldFunction):
        for particle in self.particles:
            vel = velcityFieldFunction(
                particle.position[0], particle.position[1])
            particle.velocitymag = magnitude(vel)
            if particle.velocitymag > self.maxspeed:
                particle.velocity = normalize(vel)*self.maxspeed
            else:
                particle.velocity = vel

    def updatePosition(self, dt, func, distribution="even"):
        self.distribution = distribution
        self.setVelocity(func)
        for particle in self.particles:
            particle.age += 1
            mag = particle.velocitymag
            color = self.colorMap(mag)
            if particle.age > self.lifetime:
                pos = self.distrubute()
                particle.position = pos
                particle.trail.add(particle.position, color, connected=False)
                particle.age = 0
            else:
                particle.trail.add(particle.position, color)
                particle.trail.lineWidth = self.lineWidth
                particle.lineWidth = self.lineWidth
                particle.position[0] += particle.velocity[0] * dt * self.speed
                particle.position[1] += particle.velocity[1] * dt * self.speed

    def distrubute(self):
        if self.distribution == "even":
            random1 = np.random.rand()
            random2 = np.random.rand()
            pos = [
                mapRange(random1, 0, 1, self.area[0][0], self.area[0][1]),
                mapRange(random2, 0, 1, self.area[1][0], self.area[1][1])
            ]
            return pos

        if type(self.distribution) == list:
            pos = copy(np.random.choice(self.distribution))
            pos[0] += (np.random.rand()*2-1)/10
            pos[1] += (np.random.rand()*2-1)/10
            return pos


class Particles():
    def __init__(self, n=10, area=[[-1, 1], [-1, 1]], particle_radius=0.03, particle_updater=None, m=1, speed=5, start_pos=[0, 0], color=(255, 255, 255)):
        self.position = [0, 0]
        self.n = n
        self.q = np.zeros((n, 2)) + start_pos
        self.q = np.random.rand(n, 2)*2 - 1 + start_pos
        self.q_d = (np.random.rand(n, 2)*2 - 1)*speed
        self.F = np.zeros((n, 2))
        self.m = np.array([m]*n)
        self.r = particle_radius
        self.colors = np.array([color]*n)
        if particle_updater:
            self.update_particles = particle_updater
        self.set_circles()

    def set_circles(self):
        self.circles = []
        for i, pos in enumerate(self.q):
            self.circles.append([self.r, pos, self.colors[i]])

    def update(self, screen):

        if hasattr(self, "update_particles"):
            q_updated, q_d_updated, F_updated, m_updated = self.update_particles(self.q, self.q_d, self.F, self.m)
            self.q = q_updated
            self.q_d = q_d_updated
            self.F = F_updated
            self.m = m_updated

        self.q_d += self.F * screen.dt
        self.q += self.q_d * screen.dt

        self.set_circles
