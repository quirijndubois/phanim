import numpy as np

def interp(a, b, t):
    return a + (b-a) * t

def coords2screen(res, pos, zoom):
    return np.array([
        pos[0]*zoom + res[0]/2,
        -pos[1]*zoom + res[1]/2
    ])

def screen2cords(res, pos, zoom):
    x = (pos[0] - res[0]/2)/zoom
    y = -(pos[1] - res[1]/2)/zoom
    return np.array([x, y])


def normalize(vector):
    mag = magnitude(vector)
    if mag == 0:
        return np.zeros(len(vector))
    else:
        return vector/magnitude(vector)


def magnitude(vector):
    return np.linalg.norm(vector)


def magSquared(vector):
    s = 0
    for dimension in vector:
        s += dimension**2
    return s


def distSq(a, b):  # returns distance Squared for efficiency purposes
    return magSquared(a - b)


def distance(a, b):
    return np.sqrt(distSq(a, b))


def springForce(C, l, begin, end):
    difference = begin - end
    direction = normalize(difference)
    mag = magnitude(difference) - l
    return direction * mag * C


def dampenedSpringForce(C, l, dampFactor, begin, end, vel):

    vel_direction = normalize(vel)
    vel_mag = magnitude(vel)

    difference = begin - end
    direction = normalize(difference)
    mag = magnitude(difference)

    return direction * (mag * C) - vel_direction*vel_mag*dampFactor

def pointsToLines(points, color):
    lines = []
    for i in range(len(points)-1):
        lines.append([points[i], points[i+1], color])
    return lines

def gravity(pos1, pos2, G):
    diff = [
        pos1[0] - pos2[0],
        pos1[1] - pos2[1]
    ]
    r2 = diff[0]**2 + diff[1]**2
    if r2 != 0:
        fz = G/r2
        force = [
            -diff[0]/r2**0.5*fz,
            -diff[1]/r2**0.5*fz
        ]
    else:
        force = np.array([0, 0])
    return np.array(force)


def swirlForce(pos1, pos2, G):
    diff = [
        pos1[0] - pos2[0],
        pos1[1] - pos2[1]
    ]
    r2 = diff[0]**2 + diff[1]**2
    if r2 != 0:
        fz = G/r2
        force = [
            -diff[1]/r2**0.5*fz,
            diff[0]/r2**0.5*fz
        ]
    else:
        force = np.array([0, 0])
    return np.array(force)


def calulateNormal(vector):
    return np.array(normalize([
        -vector[1],
        vector[0]
    ]))


def mapRange(value, frombegin, fromend, tobegin, toend):
    return (value-frombegin)/(fromend-frombegin) * (toend-tobegin) + tobegin


def findClosest(positions, target):
    for i in range(len(positions)):
        distance = magSquared(positions[i]-target)
        if i == 0:
            closestDistance = distance
            closestIndex = 0
        else:
            if distance < closestDistance:
                closestDistance = distance
                closestIndex = i
    return closestIndex


def calculateGradient(function, position, h=0.001):
    dx = function(position + np.array([h, 0])) - function(position)
    dy = function(position, np.array([0, h])) - function(position)
    return np.array([dx, dy])/h


def dot(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]


def calculateBezier(a, b, c, d, t):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    d = np.array(d)
    end = (
        a*(-t**3+3*t**2-3*t+1) +
        b*(3*t**3-6*t**2+3*t) +
        c*(-3*t**3+3*t**2) +
        d*(t**3)
    )
    return end


def calculateSteepness(a, b):
    rc = (a[1] - b[1]) / (a[0] - b[0])
    return rc


def calculateSlope(func, x, h=0.0000001):
    slope = (func(x+h) - func(x))/h
    return slope


def decimate(someList, desiredLength):
    decreaseFactor = int(len(someList) / desiredLength)
    returnList = []
    for i in range(len(someList)):
        if i % decreaseFactor == 0:
            returnList.append(someList[i])
    returnList.append(someList[-1])
    return returnList


def rotateToAlign(positions, desiredRotation):

    if len(positions) < 2:
        return positions  # Not enough nodes to align

    # Calculate the angle required to align the first two nodes horizontally
    delta_x = positions[1][0] - positions[0][0]
    delta_y = positions[1][1] - positions[0][1]
    angle = np.arctan2(delta_y, delta_x)

    # Create a rotation matrix
    rotation_matrix = np.array([[np.cos(-angle+desiredRotation), -np.sin(-angle+desiredRotation)],
                                [np.sin(-angle+desiredRotation),  np.cos(-angle+desiredRotation)]])

    # Apply the rotation to each position
    rotated_positions = [
        np.dot(rotation_matrix, np.array(pos)).tolist() for pos in positions]

    return rotated_positions


def calculateRotation(vector):
    delta_x = vector[0]
    delta_y = vector[1]
    return np.arctan2(delta_y, delta_x)


def randomColor(range=[0, 255], greyScale=False):
    r = int(mapRange(np.random.random(), 0, 1, range[0], range[1]))
    g = int(mapRange(np.random.random(), 0, 1, range[0], range[1]))
    b = int(mapRange(np.random.random(), 0, 1, range[0], range[1]))
    if greyScale:
        return r
    else:
        return r, g, b


def clamp(value, min, max):
    if value < min:
        return min
    elif value > max:
        return max
    else:
        return value


def round_to_power_of_2(value):
    # Calculate the logarithm base 2 of the value

    log_value = np.log2(abs(value))

    # Round the logarithmic value to the nearest integer
    rounded_log = np.ceil(log_value)

    # Calculate the closest power of 2
    result = 2 ** rounded_log

    return result, rounded_log-log_value


def elastic_collision_1d(m1, m2, v1_initial, v2_initial):
    v1_final = ((m1 - m2) / (m1 + m2)) * v1_initial + \
        ((2 * m2) / (m1 + m2)) * v2_initial
    v2_final = ((2 * m1) / (m1 + m2)) * v1_initial - \
        ((m1 - m2) / (m1 + m2)) * v2_initial

    return v1_final, v2_final


def intersecting_particles(locations, radius_squared):
    # Compute the pairwise Euclidean distance between all particles
    distances = (np.sum((locations[:, None] - locations) ** 2, axis=-1))

    # Create a boolean mask where True indicates intersecting particles
    intersecting_mask = distances <= 4 * radius_squared

    # Exclude self-intersections
    np.fill_diagonal(intersecting_mask, False)

    # Get indices of intersecting particles
    intersecting_indices = np.argwhere(intersecting_mask)

    # Convert indices to pairs and store them in a set to remove duplicates
    intersecting_pairs = set()
    for index in intersecting_indices:
        intersecting_pairs.add(tuple(sorted(index)))

    return np.array(list(intersecting_pairs))


def elastic_collision(circle1_pos, circle1_vel, circle2_pos, circle2_vel, radius, coefficient_of_restitution):
    # Step 1: Calculate relative velocity
    rel_velocity = circle2_vel - circle1_vel

    # Step 2: Calculate unit normal and unit tangent vectors
    unit_normal = (circle2_pos - circle1_pos) / \
        np.linalg.norm(circle2_pos - circle1_pos)
    # Rotate unit normal by 90 degrees
    unit_tangent = np.array([-unit_normal[1], unit_normal[0]])

    # Step 3: Resolve velocities into normal and tangential components
    v1n = np.dot(circle1_vel, unit_normal)
    v1t = np.dot(circle1_vel, unit_tangent)
    v2n = np.dot(circle2_vel, unit_normal)
    v2t = np.dot(circle2_vel, unit_tangent)

    # Step 4: Calculate new normal velocities using conservation of momentum and coefficient of restitution
    new_v1n = ((v1n * (radius - radius) + 2 * radius * v2n) /
               (2 * radius)) * coefficient_of_restitution
    new_v2n = ((v2n * (radius - radius) + 2 * radius * v1n) /
               (2 * radius)) * coefficient_of_restitution

    # Step 5: Update velocities of both circles
    new_circle1_vel = new_v1n * unit_normal + v1t * unit_tangent
    new_circle2_vel = new_v2n * unit_normal + v2t * unit_tangent

    # Step 6: Calculate new positions of circles post-collision, ensuring non-overlapping positions
    separation = np.linalg.norm(circle2_pos - circle1_pos)
    overlap = 2 * radius - separation
    if overlap > 0:
        correction = overlap / 2
        correction_vector = unit_normal * correction
        circle1_pos -= correction_vector
        circle2_pos += correction_vector

    return new_circle1_vel, new_circle2_vel, circle1_pos, circle2_pos
