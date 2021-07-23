from math import sqrt, pow

def string_to_bool(s):
    if s in ["False", "0"]:
        return False
    else:
        return True

def dot(a, b):
    return a[0] * b[0] + a[1] * b[1]

def mag(v):
    return sqrt(pow(v[0], 2) + pow(v[1], 2))

def dist(ax, ay, bx, by):
    return mag((bx - ax, by - ay))

def line_circle_intersect(ax, ay, bx, by, cx, cy, r):
    # Change coordinate origin to be at the circle center
    x1 = ax - cx
    y1 = ay - cy
    x2 = bx - cx
    y2 = by - cy

    # Square the radius to avoid needing any square roots
    r2 = r * r

    # Check if endpoints are in the circle
    if (x1 * x1 + y1 * y1 <= r2):
        return True
    if (x2 * x2 + y2 * y2 <= r2):
        return True

    # Calculate the line segment length squared
    len2 = (x1 - x2) * (x1 - x2) + (y1 - y2)*(y1 - y2)

    # find the perpendicular vector to the line segment
    nx = y2 - y1
    ny = x1 - x2

    # find the distance squared from center to line, times len2
    dist2 = nx * x1 + ny * y1
    dist2 = dist2 * dist2

    # Check if full line intersects the circle. If not, return false
    if (dist2 > len2 * r2):
        return False

    # Calculate the distance from (x1,y1) to the point of closest approach) times the segment length
    index = (x1*(x1 - x2) + y1*(y1 - y2)) 

    # Check if point of closest approach is inside the segment.
    if (index < 0):
        return False
    if (index > len2):
        return False
    return True