import numpy as np
from .functions import *
from copy import copy

class Physics():
    @staticmethod
    def constraintSolver(node,functions,force,dt):
        node.velocity = vadd(node.velocity,np.array(force)*dt)
        p = copy(node.position)
        node.position = vadd(node.position,node.velocity*dt)
        Physics.satisfyContraints(node,functions)
        newVelocity = diff(node.position,p)/dt
        node.velocity = newVelocity

    @staticmethod
    def satisfyContraints(node,functions):
        for function in functions:
            slope = -calculateGradient(function,node.position)
            newPosition = vadd(normalize(slope)*function(node.position),node.position)
            node.position = newPosition
