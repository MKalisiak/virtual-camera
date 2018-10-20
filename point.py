import numpy as np


class Point(object):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

    def transform(self, matrix):
        vector = np.array([self.x, self.y, self.z, 1], dtype=float)
        result = np.matmul(matrix, vector)
        self.x = result[0]
        self.y = result[1]
        self.z = result[2]
