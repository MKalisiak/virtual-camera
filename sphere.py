from point import Point3D, Point2D
import pygame
import colors
from sympy.solvers import solve
from sympy import Symbol
import numpy as np
from enum import Enum
from material import Material
from phong import Phong


class ColorPart(Enum):
    Red = 0
    Green = 1
    Blue = 2


class Sphere(object):
    def __init__(self, center: Point3D, radius: int, material: Material):
        self.center = center
        self.radius = radius
        self.material = material

    def draw(self, scene):
        if self.center.z <= 0:
            return

        projected_center = self.center.project(scene)
        projected_radius = self.radius * scene.d / self.center.z

        projected_center = (int(projected_center.x), int(projected_center.y))
        projected_radius = int(projected_radius)

        pygame.draw.circle(scene.canvas, colors.green, projected_center, projected_radius, 0)

        pixels = pygame.surfarray.pixels3d(scene.canvas)

        phong = Phong(scene, self, scene.light)

        counter = 0
        number_of_pixels = scene.height * scene.width * 3

        # index = [x, y, ( r | g | b )]
        # pixel = <color value>
        for index, pixel in np.ndenumerate(pixels):
            if self.is_pixel_green(pixels[index[0], index[1], :]):
                point = self.reverse_project(scene, Point2D(index[0], index[1]))
                intensity = phong.compute(point)
                intensity = np.clip(intensity, 0, 255) / 255
                pixels[index[0], index[1], :] = np.clip((self.material.color + scene.light.color) * intensity, 0, 255)
            counter += 1
            if counter % (number_of_pixels / 100) == 0:
                print(f'{counter / number_of_pixels * 100}%')

    @staticmethod
    def is_pixel_green(pixel):
        return pixel[ColorPart.Red.value] == 0 and pixel[ColorPart.Green.value] == 255 and pixel[ColorPart.Blue.value] == 0

    def transform(self, matrix):
        self.center.transform(matrix)

    def reverse_project(self, scene, point: Point2D):
        x_p = point.x
        y_p = point.y

        x_c = self.center.x
        z_c = self.center.z
        y_c = self.center.y
        r = self.radius

        d = scene.d
        x_offset = scene.width / 2
        y_offset = scene.height / 2

        a = (((x_p - x_offset) ** 2 + (y_p - y_offset) ** 2) / d **2) + 1
        b = (((-2 * x_c * (x_p - x_offset)) - (2 * y_c * (y_p - y_offset))) / d) - (2 * z_c)
        c = x_c ** 2 + y_c ** 2 + z_c ** 2 - r ** 2

        possible_z = np.roots([a, b, c])

        z = min(possible_z)

        z = float(z)

        x = (x_p - x_offset) * z / d
        y = (y_p - y_offset) * z / d

        reversed_point = Point3D(x, y, z)

        return reversed_point


