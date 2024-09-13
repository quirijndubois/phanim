import numpy as np
import math


def interp(a, b, t):
    return a + (b-a) * t


def coords2screen(res, pos, pixelsPerUnit):
    return np.array([
        pos[0]*pixelsPerUnit + res[0]/2,
        -pos[1]*pixelsPerUnit + res[1]/2
    ])


def screen2cords(res, pos, pixelsPerUnit):
    x = (pos[0] - res[0]/2)/pixelsPerUnit
    y = -(pos[1] - res[1]/2)/pixelsPerUnit
    return np.array([x, y])


def normalize(vector, mag=None):
    vector = np.array(vector)
    if mag == None:
        mag = magnitude(vector)

    if mag == 0:
        return np.zeros(len(vector))
    else:
        return vector/mag


def magnitude(vector):
    if len(vector) == 2:
        return math.sqrt(vector[0]**2+vector[1]**2)
    else:
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
    difference = begin - end
    direction = normalize(difference)
    mag = magnitude(difference) - l

    vel_along_spring = dot(vel, direction) * direction

    spring_force = direction * (mag * C)
    damping_force = -vel_along_spring * dampFactor

    return spring_force + damping_force


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


def calculateNormal(vector):
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


def is_point_in_polygon(point, polygon):
    """
    Check if a 2D point is inside a polygon.

    Parameters:
    - point: A tuple (x, y) representing the point.
    - polygon: A list of tuples [(x1, y1), (x2, y2), ...] representing the vertices of the polygon.

    Returns:
    - True if the point is inside the polygon, False otherwise.
    """
    x, y = point
    n = len(polygon)
    inside = False

    # Iterate over edges of the polygon
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]  # Wrap around to the first vertex

        # Check if the point is inside the y-bounds of the edge
        if min(y1, y2) < y <= max(y1, y2):
            # Compute the x coordinate of the intersection of the edge with the horizontal ray
            xinters = (y - y1) * (x2 - x1) / (y2 - y1) + x1

            # If the point is to the left of the intersection point, toggle the inside flag
            if x < xinters:
                inside = not inside

    return inside


def distance_point_to_line(p1, p2, p):
    """
    Calculate the perpendicular distance from point p to the line segment p1-p2.
    """
    line_len = np.linalg.norm(np.array(p2) - np.array(p1))
    if line_len == 0:
        return np.linalg.norm(np.array(p) - np.array(p1))

    t = max(0, min(1, np.dot(np.array(p) - np.array(p1),
            np.array(p2) - np.array(p1)) / line_len**2))
    projection = np.array(p1) + t * (np.array(p2) - np.array(p1))
    return np.linalg.norm(np.array(p) - projection)


def closest_point_on_line(p, a, b):
    """
    Finds the closest point on the line segment AB to point P.
    P, A, B are all tuples representing 2D points (x, y).
    """
    # Vector from A to P
    AP = (p[0] - a[0], p[1] - a[1])
    # Vector from A to B
    AB = (b[0] - a[0], b[1] - a[1])

    # Squared length of AB
    AB_length_squared = AB[0]**2 + AB[1]**2
    if AB_length_squared == 0:
        # A and B are the same point
        return a

    # Projection factor t of AP onto AB normalized to [0, 1]
    t = max(0, min(1, (AP[0] * AB[0] + AP[1] * AB[1]) / AB_length_squared))

    # Closest point on the line segment
    closest_point = (a[0] + t * AB[0], a[1] + t * AB[1])
    return closest_point+calculateNormal(AB)*0.01


def closest_point_outside_polygon(point, polygon):
    """
    Given a point and a polygon, if the point is inside the polygon, returns the closest point
    on the polygon's edges (i.e., outside of the polygon). If the point is not inside, returns None.

    :param point: Tuple (x, y) representing the 2D point to check.
    :param polygon: List of tuples [(x1, y1), (x2, y2), ..., (xn, yn)] representing the polygon vertices.
    :return: Tuple representing the closest point outside the polygon or None if the point is outside.
    """
    if not is_point_in_polygon(point, polygon):
        return point  # Point is already outside

    min_distance = float('inf')
    closest_point = None

    # Iterate through each edge of the polygon
    for i in range(len(polygon)):
        a = polygon[i]
        # Wrap around to form a closed polygon
        b = polygon[(i + 1) % len(polygon)]

        # Find the closest point on the current edge
        candidate_point = closest_point_on_line(point, a, b)

        # Calculate the distance between the point and the candidate point
        distance = math.dist(point, candidate_point)

        if distance < min_distance:
            min_distance = distance
            closest_point = candidate_point

    return closest_point


def polygon_area(polygon):
    """
    Calculate the area of a polygon using the Shoelace formula.

    Parameters:
    - polygon: A list of tuples [(x1, y1), (x2, y2), ...] representing the vertices of the polygon.

    Returns:
    - The area of the polygon.
    """
    n = len(polygon)
    area = 0

    # Iterate over pairs of vertices
    for i in range(n):
        x1, y1 = polygon[i]
        x2, y2 = polygon[(i + 1) % n]  # Wrap around to the first vertex

        # Add the cross-product of the current vertex and the next
        area += x1 * y2 - x2 * y1

    # Take the absolute value and divide by 2
    area = abs(area) / 2
    return area
