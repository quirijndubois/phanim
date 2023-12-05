import phanim
import numpy as np

class Particles():
    def __init__(self,n=150,lifetime=20,area=[[-5,5],[-5,5]],radius = 0,distribution = "even",trails=True,lineWidth=2,speed=100,maxspeed=2e-2,fadingtime=2):
        self.lifetime = lifetime
        self.area = area
        self.distribution = distribution
        self.particles = []
        self.lineWidth = lineWidth
        self.speed = speed
        self.maxspeed = maxspeed
        for i in range(n):
            random1 = np.random.rand()
            random2 = np.random.rand()
            pos = [
                phanim.mapRange(random1, 0, 1,self.area[0][0],self.area[0][1]),
                phanim.mapRange(random2, 0, 1,self.area[1][0],self.area[1][1])
            ]
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

    def updatePosition(self,dt,func):
        self.setVelocity(func)
        for particle in self.particles:
            particle.age +=1
            mag = particle.velocitymag
            if mag < 1 and mag > 0:
                color = (
                    phanim.interp(0, 255,mag**0.5),
                    phanim.interp(55, 0,mag),
                    phanim.interp(200, 0,mag**2),
                )
            else:
                color = (255,0,0)
            if particle.age > self.lifetime:
                random1 = np.random.rand()
                random2 = np.random.rand()
                pos = [
                    phanim.mapRange(random1, 0, 1,self.area[0][0],self.area[0][1]),
                    phanim.mapRange(random2, 0, 1,self.area[1][0],self.area[1][1])
                ]
                particle.position = pos
                particle.trail.add(particle.position,color,connected=False)
                particle.age = 0
            else:
                particle.trail.add(particle.position,color)
                particle.trail.lineWidth = self.lineWidth
                particle.lineWidth = self.lineWidth
                particle.position[0] +=  particle.velocity[0] * dt * self.speed
                particle.position[1] +=  particle.velocity[1] * dt * self.speed
