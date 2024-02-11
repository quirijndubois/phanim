from phanim import *

particle_amount = 100
particle_speed = 50
particle_mass = 0.001
particle_radius = 0.05

plate_force = 10
plate_mass = 2

substeps = 10

bounce_radius = particle_radius/100
bounce_radius_squared = bounce_radius**2

s = Screen(grid=True, panning=True, fullscreen=False)

plate_node = Node(pos=[0, 0], interactivityType="force")
plate = Line(start=[0, -2], stop=[0, 2])
plate.position = plate_node.position

box = Rectangle(position=[18,0],width=44,height=4)

s.play(Create(plate), Create(box), Create(plate_node))

def update(s):
    f = [-plate_force, 0]

    plate_node.eulerODESolver(f, s.dt)
    plate_node.velocity[1] = 0
    plate_node.position[1] = 0
    plate.position = plate_node.position

    if plate_node.position[0] > 40:
        plate_node.position[0] = 40 - 0.01
        plate_node.velocity[0] *=-1

def update_particle_collisions(s):
    intersection = intersecting_particles(particles.q, bounce_radius_squared)

    if len(intersection) > 0:
        for particle_pair in intersection:
            v1, v2, p1, p2 = elastic_collision(
                particles.q[particle_pair[0]],
                particles.q_d[particle_pair[0]],
                particles.q[particle_pair[1]],
                particles.q_d[particle_pair[1]],
                bounce_radius,
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

    # Handle left wall boundary
    mask_left = x[:, 0] < -4
    v[mask_left, 0] *= -1
    x[mask_left, 0] = -3.9

    # Handle right wall boundary (assuming plate_node is a global variable)
    mask_right = x[:, 0] > plate_node.position[0] -0.05
    v1, v2 = elastic_collision_1d(particle_mass, plate_mass, v[mask_right, 0], plate_node.velocity[0])
    v[mask_right, 0] = v1
    if len(v2)>0:
        plate_node.velocity[0] = v2[0]
    x[mask_right, 0] = plate_node.position[0] - 0.05

    # Handle bottom boundary
    mask_bottom = x[:, 1] < -2
    v[mask_bottom, 1] *= -1
    x[mask_bottom, 1] = -1.99

    # Handle top boundary
    mask_top = x[:, 1] > 2
    v[mask_top, 1] *= -1
    x[mask_top, 1] = 1.99

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
