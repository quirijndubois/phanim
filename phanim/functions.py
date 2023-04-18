import numpy as np

def interp(a,b,t):
    return a + (b-a) * t

def interp2d(a,b,t):
    return np.array([interp(a[0], b[0], t),interp(a[1], b[1], t)])

def coords2screen(res:list,pos:list,zoom):
    return [
        pos[0]*zoom + res[0]/2,
        -pos[1]*zoom + res[1]/2
    ]

def screen2cords(res:list,pos:list,zoom):
    x = (pos[0] - res[0]/2)/zoom
    y = -(pos[1] - res[1]/2)/zoom
    return [x,y]

def normalize(vector):
    s = 0
    for dimension in vector:
        s += dimension**2
    s = s**(0.5)
    newVector = []
    for dimension in vector:
        newVector.append(dimension/s)
    return np.array(newVector)

def difference(v1,v2):
    return np.array([
        v1[0] - v2[0],
        v1[1] - v2[1]
    ])

diff = difference

def magnitude(vector):
    s = 0
    for dimension in vector:
        s += dimension**2
    return s**(0.5)

def magSquared(vector):
    s = 0
    for dimension in vector:
        s += dimension**2
    return s

def distSq(a,b): #returns distance Squared for efficiency purposes
    return magSquared(diff(a,b))

def distance(a,b):
    return np.sqrt(distSq(a,b))

def springForce(C,l,begin,end):
    difference = np.array(begin) - np.array(end)
    direction = np.array(normalize(difference))
    mag = magnitude(difference) - l
    return direction * mag * C

def vadd(*args):
    result = [0,0]
    for arg in args:
        result[0] += arg[0] 
        result[1] += arg[1]
    return np.array(result)

def pointsToLines(points,color):
    lines = []
    for i in range(len(points)-1):
        lines.append([points[i],points[i+1],color])
    return lines

def gravity(pos1,pos2,G):
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
        force = np.array([0,0])
    return np.array(force)

def swirlForce(pos1,pos2,G):
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
        force = np.array([0,0])
    return np.array(force)

def calulateNormal(vector):
    return np.array(normalize([
        -vector[1],
        vector[0]
    ]))

def mapRange(value,frombegin,fromend,tobegin,toend):
    return (value-frombegin)/(fromend-frombegin) * (toend-tobegin) + tobegin

def findClosest(positions,target):
    for i in range(len(positions)):
        distance = magSquared(diff(positions[i],target))
        if i == 0:
            closestDistance = distance
            closestIndex = 0
        else:
            if distance < closestDistance:
                closestDistance = distance
                closestIndex = i
    return closestIndex

def calculateGradient(function,position,h=0.001):
    dx = function(vadd(position,[h,0])) - function(position)
    dy = function(vadd(position,[0,h])) - function(position)
    return np.array([dx,dy])/h

def dot(vec1,vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]

def calculateBezier(a,b,c,d,t):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    d = np.array(d)
    end = (
        a*(-t**3+3*t**2-3*t+1)+
        b*(3*t**3-6*t**2+3*t)+
        c*(-3*t**3+3*t**2)+
        d*(t**3)
    )
    return end

