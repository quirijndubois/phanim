from phanim import *
import numpy as np

s = Screen()

beam = Beam(length=4,position = [-1,0])

node = Node(radius=0.1)

s.add(beam)
s.play(Create(node))

s.makeInteractive(beam)

def update(s):
    force = -interp(beam.getLeft(),beam.getRight(),0.75)*100000
    beam.applyForce(force,[0,0])
    beam.eulerODESolver(s.dt)

s.addUpdater(update,substeps=100)

s.run()  
