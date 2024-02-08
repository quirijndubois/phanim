from phanim import *

particle_amount = 500
particle_speed = 5
particle_mass = 0.02
particle_radius = 0.05

plate_force = 10
plate_mass = 2

substeps = 10


s = Screen(grid=True, panning=True, fullscreen=False)

plate_node = Node(pos=[1, 0], interactivityType="force")
plate = Line(start=[0, -2], stop=[0, 2])
plate.position = plate_node.position

box = Curve(points=[[4, 2], [-4, 2], [-4, -2], [4, -2]], color=color.blue)

s.play(Create(plate), Create(box), Create(plate_node))


def update(s):
    f = [-plate_force, 0]

    plate_node.eulerODESolver(f, s.dt)
    plate_node.velocity[1] = 0
    plate_node.position[1] = 0
    plate.position = plate_node.position


def update_particle_collisions(s):
    intersection = intersecting_particles(particles.q, particles.r)

    if len(intersection) > 0:
        for particle_pair in intersection:
            v1, v2, p1, p2 = elastic_collision(
                particles.q[particle_pair[0]],
                particles.q_d[particle_pair[0]],
                particles.q[particle_pair[1]],
                particles.q_d[particle_pair[1]],
                particles.r,
                1
            )
            particles.q[particle_pair[0]] = p1
            particles.q_d[particle_pair[0]] = v1
            particles.q[particle_pair[1]] = p2
            particles.q_d[particle_pair[1]] = v2


s.makeInteractive(plate_node)

s.addUpdater(
    update
)


def update_particles(x, v, F, m):

    if x[0] < -4:
        v[0] *= -1
        x[0] = -3.99

    if x[0] > plate_node.position[0]-0.05:

        v1, v2 = elastic_collision_1d(
            m, plate_mass, v[0], plate_node.velocity[0])
        v[0] = v1
        plate_node.velocity[0] = v2

        x[0] = plate_node.position[0] - 0.05

    if x[1] < -2:
        v[1] *= -1
        x[1] = -1.99

    if x[1] > 2:
        v[1] *= -1
        x[1] = 1.99

    return x, v, F, m


particles = Particles(
    n=particle_amount,
    particle_updater=update_particles,
    speed=particle_speed,
    m=particle_mass,
    start_pos=[-2, 0],
    particle_radius=particle_radius,
)


s.play(Add(particles))


s.addUpdater(particles.update, substeps=substeps)
s.addUpdater(update_particle_collisions)

s.run()
