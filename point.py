import numpy as np


class Point3D(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def __repr__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def transform(self, matrix):
        vector = np.array([self.x, self.y, self.z, 1], dtype=float)
        result = np.matmul(matrix, vector)
        self.x = result[0]
        self.y = result[1]
        self.z = result[2]

    def project(self, scene):
        projected_x = scene.width / 2 + self.x * scene.d / self.z
        projected_y = scene.height / 2 + self.y * scene.d / self.z
        return Point2D(projected_x, projected_y)

    def add_point(self, point):
        self.x += point.x
        self.y += point.y
        self.z += point.z
        return self

    def divide_by_scalar(self, divider):
        self.x /= divider
        self.y /= divider
        self.z /= divider
        return self

class Point2D(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y
