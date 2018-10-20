from point import Point
from math import sin, cos
import numpy as np


class Cuboid(object):
    def __init__(self, start_point, width, depth, height):
        p = start_point
        self.bottom_0 = Point(p.x, p.y, p.z)
        self.bottom_1 = Point(p.x + width, p.y, p.z)
        self.bottom_2 = Point(p.x + width, p.y, p.z + depth)
        self.bottom_3 = Point(p.x, p.y, p.z + depth)

        self.top_0 = Point(p.x, p.y + height, p.z)
        self.top_1 = Point(p.x + width, p.y + height, p.z)
        self.top_2 = Point(p.x + width, p.y + height, p.z + depth)
        self.top_3 = Point(p.x, p.y + height, p.z + depth)

        self.points = [self.bottom_0, self.bottom_1, self.bottom_2, self.bottom_3,
                       self.top_0, self.top_1, self.top_2, self.top_3]

        self.edges = [(0, 1), (1, 2), (2, 3), (3, 0), (0, 4), (1, 5), (2, 6), (3, 7), (4, 5), (5, 6), (6, 7), (7, 4)]

    def draw(self, scene):
        for edge in self.edges:
            start, end = self.points[edge[0]], self.points[edge[1]]
            if start.z <= 0 or end.z <= 0:
                continue
            start_x, start_y = self.project(start, scene)
            end_x, end_y = self.project(end, scene)
            scene.canvas.create_line(start_x, start_y, end_x, end_y, fill="white")

    def translate(self, distance, axis):
        matrix = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]], dtype=float)

        matrix[axis, 3] = distance
        for point in self.points:
            point.transform(matrix)

    def rotate(self, angle, axis):
        matrix = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]], dtype=float)

        if axis == 0:
            matrix[1:3, 1:3] = np.array([[cos(angle), -1 * sin(angle)],
                                         [sin(angle), cos(angle)]])
        elif axis == 1:
            matrix[0:3, 0:3] = np.array([[cos(angle), 0, sin(angle)],
                                         [0, 1, 0],
                                         [-1 * sin(angle), 0, cos(angle)]])
        elif axis == 2:
            matrix[0:2, 0:2] = np.array([[cos(angle), -1 * sin(angle)],
                                         [sin(angle), cos(angle)]])

        for point in self.points:
            point.transform(matrix)

    @staticmethod
    def project(point, scene):
        projected_x = scene.width / 2 + point.x * scene.d / point.z
        projected_y = scene.height / 2 + point.y * scene.d / point.z
        return projected_x, projected_y



