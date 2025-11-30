import random
import math

def mg_distance_mg(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.hypot(x2 - x1, y2 - y1)

def mg_angle_mg(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return math.degrees(math.atan2(y2 - y1, x2 - x1))

def mg_length_sqrt_mg(dx, dy):
    return math.sqrt(dx*dx + dy*dy)

def mg_random_color_mg():
    r = random.randint(0,255)
    g = random.randint(0,255)
    b = random.randint(0,255)
    return f"#{r:02x}{g:02x}{b:02x}"
