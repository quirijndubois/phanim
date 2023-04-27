from phanim import *

scr = Screen([1360,765])

grids = Grid(1,1,10,10,position=[0.5,0.5],color=(50,50,50)),Grid(1,1,10,10)

circle = Circle(color=color.purple,radius=2)

square = Rectangle(color=color.red)
square2 = Quadrilateral(corners=[[1,1.5],[-1,0.5],[-2,-1],[2,-2]],color=color.blue)

graph = Graph(color=color.green)
x = np.linspace(-2,2,100)
graph.setData(x, np.sin(x*3)+x)
axes = Axes()

scr.play(Create(grids[1]))
scr.play(Create(grids[0]))
scr.play(Create(circle,duration=120))
scr.play(Transform(circle,square))
scr.play(Transform(circle,square2))
scr.play(Transform(circle,graph),Create(axes))
scr.play(Destroy(grids[0]),Destroy(grids[1]))
scr.play(Move(scr.camera,[1,1]))
scr.run()
