from phanim import *

s = Screen(grid=True,panning=True)

plate_node = Node(pos=[4,0],interactivityType="force")
plate = Line(start=[0,-2],stop=[0,2])
plate.position = plate_node.position

spring = DottedLine()

box = Curve(points=[[4,2],[-4,2],[-4,-2],[4,-2]],color=color.blue)

s.play(Create(spring),Create(plate),Create(box),Create(plate_node))


def update(s):
    f = dampenedSpringForce(10,0,0,[1,0],plate_node.position,plate_node.velocity)

    plate_node.eulerODESolver(f,s.dt)
    plate_node.velocity[1] = 0
    plate_node.position[1] = 0
    plate.position = plate_node.position
    spring.setEnds([1,0],plate_node.position)

    if plate_node.position[0] < -3:
         plate_node.position[0] = -3

s.makeInteractive(plate_node)

s.addUpdater(
    update
)
def elastic_collision(m1, m2, v1_initial, v2_initial):

    v1_final = ((m1 - m2) / (m1 + m2)) * v1_initial + ((2 * m2) / (m1 + m2)) * v2_initial
    v2_final = ((2 * m1) / (m1 + m2)) * v1_initial - ((m1 - m2) / (m1 + m2)) * v2_initial

    return v1_final, v2_final

def update_particles(x,v,F,m):


    if x[0] < -4:
        v[0] *= -1
        x[0] = -3.99

    if x[0] > plate_node.position[0]-0.05:

        v1,v2 = elastic_collision(m,2,v[0],plate_node.velocity[0])
        v[0] = v1
        plate_node.velocity[0] = v2

        x[0] = plate_node.position[0] - 0.05

    if x[1] < -2:
        v[1] *= -1
        x[1] = -1.99

    if x[1] > 2:
        v[1] *= -1
        x[1] = 1.99

    return x,v,F,m

particles = Particles(n=1000,particle_updater=update_particles,speed=5,m=0.2)


s.play(Add(particles))


s.addUpdater(particles.update,substeps=1)


s.run()