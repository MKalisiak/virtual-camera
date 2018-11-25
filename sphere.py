from point import Point3D, Point2D
import pygame
import colors
from sympy.solvers import solve
from sympy import Symbol
import numpy as np
from enum import Enum


class ColorPart(Enum):
    Red = 0
    Green = 1
    Blue = 2


class Sphere(object):
    def __init__(self, center: Point3D, radius: int):
        self.center = center
        self.radius = radius

    def draw(self, scene):
        print(self.center)
        if self.center.z <= 0:
            return

        projected_center = self.center.project(scene)
        projected_radius = self.radius * scene.d / self.center.z

        projected_center = (int(projected_center.x), int(projected_center.y))
        projected_radius = int(projected_radius)

        print(projected_center)

        pygame.draw.circle(scene.canvas, colors.green, projected_center, projected_radius, 0)
        # pygame.draw.circle(scene.canvas, colors.white, projected_center, projected_radius, 1)

        pixels = pygame.surfarray.pixels3d(scene.canvas)
        print(pixels.shape)
        counter = 0
        for index, pixel in np.ndenumerate(pixels):
            if index[2] == ColorPart.Green.value and pixel == 255:
                pixels[index[0], index[1], :] = np.array([255, 0, 0])
                point = self.reverse_project(scene, Point2D(index[0], index[1]))
                print(f'{point}, {self.center}')
                print(type(point.x))
                counter += 1
                if counter > 100:
                    break


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

        z = Symbol('z')
        possible_z = solve((x_p * z / d - x_c) ** 2 + (y_p * z / d - y_c) ** 2 + (z - z_c) ** 2 - r ** 2, z)

        print(possible_z)
        z = min(possible_z)

        z = float(z)

        x = x_p * z / d
        y = y_p * z / d

        reversed_point = Point3D(x, y, z)

        return reversed_point
