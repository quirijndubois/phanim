import phanim
import numpy as np
from phanim.color import NaturalColorMap
import random
from copy import copy

class Particles():
    def __init__(self,n=150,lifetime=20,area=[[-5,5],[-5,5]],radius = 0,colorMap=NaturalColorMap,trails=True,lineWidth=2,speed=100,maxspeed=2e-2,fadingtime=2,distribution = "even"):
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
            node = phanim.Node(pos=pos,radius=radius)
            node.age = np.random.randint(0,self.lifetime)
            if trails:
                node.trail = phanim.Trail(length=self.lifetime*fadingtime)
            self.particles.append(node)
    
    def setVelocity(self,velcityFieldFunction):
        for particle in self.particles:
            vel = velcityFieldFunction(particle.position[0],particle.position[1])
            particle.velocitymag = phanim.magnitude(vel)
            if particle.velocitymag > self.maxspeed:
                particle.velocity = phanim.normalize(vel)*self.maxspeed
            else: 
                particle.velocity = vel

    def updatePosition(self,dt,func,distribution = "even"):
        self.distribution = distribution
        self.setVelocity(func)
        for particle in self.particles:
            particle.age +=1
            mag = particle.velocitymag
            color = self.colorMap(mag)
            if particle.age > self.lifetime:
                pos = self.distrubute()
                particle.position = pos
                particle.trail.add(particle.position,color,connected=False)
                particle.age = 0
            else:
                particle.trail.add(particle.position,color)
                particle.trail.lineWidth = self.lineWidth
                particle.lineWidth = self.lineWidth
                particle.position[0] +=  particle.velocity[0] * dt * self.speed
                particle.position[1] +=  particle.velocity[1] * dt * self.speed

    def distrubute(self):
        if self.distribution == "even":
            random1 = np.random.rand()
            random2 = np.random.rand()
            pos = [
                phanim.mapRange(random1, 0, 1,self.area[0][0],self.area[0][1]),
                phanim.mapRange(random2, 0, 1,self.area[1][0],self.area[1][1])
            ]
            return pos
        
        if type(self.distribution) == list:
            pos = copy(random.choice(self.distribution))
            pos[0]+=(np.random.rand()*2-1)/10
            pos[1]+=(np.random.rand()*2-1)/10
            return pos