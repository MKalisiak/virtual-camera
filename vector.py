from point import Point3D
from math import sqrt


class Vector3D(object):
    def __init__(self, start: Point3D, end: Point3D):
        self.start = start
        self.end = end

    def __repr__(self):
        return f'{self.start}, {self.end}'

    def length(self):
        return sqrt((self.start.x - self.end.x) ** 2 + (self.start.y - self.end.y) ** 2 + (self.start.z - self.end.z) ** 2)

    def move(self, new_start: Point3D):
        new_end = Point3D(self.end.x - self.start.x + new_start.x,
                          self.end.y - self.start.y + new_start.y,
                          self.end.z - self.start.z + new_start.z,)
        return Vector3D(new_start, new_end)

    def resize(self, new_length):
        old_length = self.length()
        new_x = (self.end.x - self.start.x) / old_length * new_length + self.start.x
        new_y = (self.end.y - self.start.y) / old_length * new_length + self.start.y
        new_z = (self.end.z - self.start.z) / old_length * new_length + self.start.z
        return Vector3D(self.start, Point3D(new_x, new_y, new_z))

    def dot(self, vector):
        return ((self.end.x - self.start.x) * (vector.end.x - vector.start.x) +
                (self.end.y - self.start.y) * (vector.end.y - vector.start.y) +
                (self.end.z - self.start.z) * (vector.end.z - vector.start.z))

    def project_point(self, point: Point3D) -> Point3D:
        vector = Vector3D(self.start, point)
        scalar_projection = self.dot(vector) / self.length()
        return self.resize(scalar_projection).end

    def reflect_point(self, point: Point3D) -> Point3D:
        projected = self.project_point(point)
        projecting_vector = Vector3D(point, projected)
        return point.add_vector(projecting_vector.resize(projecting_vector.length() * 2))
