# import numpy as np
from .functions import *
from copy import copy

class Physics():
    @staticmethod
    def constraintSolver(nodes, constraints, dt):
        for node in nodes:
            Physics.integrate(node, dt)
            pass

        for constraint in constraints:
            Physics.satisfyContraints(constraint)

    @staticmethod
    def integrate(node, dt):
        node.velocity = (node.velocity+node.force) * dt
        node.position = (node.position+node.velocity) * dt

    @staticmethod
    def satisfyContraints(constraint):
        for node in constraint.nodes:
            correction = Physics.calculateCorrection(constraint, node)
            node.position += correction

    @staticmethod
    def calculateCorrection(constraint, node):
        C = constraint.evaluate()  # Constraint function value
        J = constraint.gradient(node)  # Gradient of the constraint function
        print(C)
        print(J)

        correction = -normalize(J)*C/2

        return correction

class DoublePendulumConstraint:
    def __init__(self, node1, node2, length):
        self.nodes = [node1, node2]
        self.length = length

    def evaluate(self):
        distance = self.nodes[0].position-self.nodes[1].position
        mag = magnitude(distance)
        return mag-self.length

    def gradient(self, node):
        dif = self.nodes[0].position-self.nodes[1].position
        return normalize(dif) if node == self.nodes[0] else -normalize(dif)