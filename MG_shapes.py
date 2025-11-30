from MG_utils import mg_distance_mg, mg_angle_mg
import math

class MGShape:
    def __init__(self, color="#000000", width=3):
        self.points = []
        self.color = color
        self.width = width

    def add_point(self, pt):
        self.points.append(pt)

    def bounding_box(self):
        if not self.points:
            return (0,0,0,0)
        xs = [p[0] for p in self.points]
        ys = [p[1] for p in self.points]
        return (min(xs), min(ys), max(xs), max(ys))

    def draw_on(self, canvas):
        if len(self.points) < 2:
            return
        pts = self.points
        for a, b in zip(pts[:-1], pts[1:]):
            canvas.create_line(a[0], a[1], b[0], b[1], fill=self.color, width=self.width, capstyle="round", joinstyle="round", smooth=True)

    def length(self):
        if len(self.points) < 2:
            return 0
        total = 0
        for a, b in zip(self.points[:-1], self.points[1:]):
            total += mg_distance_mg(a, b)
        return total

    def centroid(self):
        if not self.points:
            return (0,0)
        x = sum(p[0] for p in self.points)/len(self.points)
        y = sum(p[1] for p in self.points)/len(self.points)
        return (x,y)
