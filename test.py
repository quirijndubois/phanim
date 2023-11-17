from phanim import *

s = Screen(fullscreen=True,panning=True)

circles = [
    Node(pos=[-1,2]),
    Node(pos=[-1,1]),
    Node(pos=[-1,0]),
    Node(pos=[-1,-1]),
    Node(pos=[-1,-2]),
    ]

s.play(Create(DGrid()))
s.play(laggedStart(*[Create(node) for node in circles]))
s.play(*[Shift(node,[2,0]) for node in circles])

s.play(laggedStart(*[Shift(node,[-2,0]) for node in circles]))

s.run()
