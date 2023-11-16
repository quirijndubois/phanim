from phanim import *

s = Screen(fullscreen=True)

# circles = [
#     Node(pos=[-1,2]),
#     Node(pos=[-1,1]),
#     Node(pos=[-1,0]),
#     Node(pos=[-1,-1]),
#     Node(pos=[-1,-2]),
#     ]
# s.play(*[Create(node) for node in circles])
# s.play(laggedStart(*[Shift(node,[2,0]) for node in circles]))

# s.play(Move(circles[2],[0,0]))

circle = Circle()

s.play(Create(circle))
s.play(laggedStart(Move(circle,[1,0])))

s.run()
