from point import Point3D
from vector import Vector3D


class Phong(object):
    def __init__(self, scene, sphere, light):
        self.scene = scene
        self.sphere = sphere
        self.light = light

    def compute(self, point: Point3D):
        return (self.sphere.material.k_a * self.light.ambient_intensity +
                self.sphere.material.k_d * self.light.directional_intensity * self.normal(point).dot(self.light_vector(point)) +
                self.sphere.material.k_s * self.light.directional_intensity * self.observer_vector(point).dot(self.reflection_vector(point)) ** self.sphere.material.n)

    def normal(self, point: Point3D) -> Vector3D:
        return Vector3D(self.sphere.center, point).move(point).resize(1)

    def light_vector(self, point: Point3D) -> Vector3D:
        return Vector3D(point, self.light.position).resize(1)

    def observer_vector(self, point: Point3D) -> Vector3D:
        return Vector3D(point, self.scene.camera).resize(1)

    def reflection_vector(self, point: Point3D) -> Vector3D:
        return Vector3D(point, self.normal(point).reflect_point(self.light.position)).resize(1)
