import math
from cuboid import Cuboid
from sphere import Sphere
from light_source import LightSource
from point import Point3D
from math import sin, cos
import numpy as np
from axis import Axis
from painter import Painter
import pygame
import colors
from material import Material


class Scene(object):
    def __init__(self):
        self.width = 300
        self.height = 300
        self.move_step = 2
        self.zoom_step = 10
        self.rotate_step = math.pi / 18

        self.canvas = pygame.display.set_mode((self.width, self.height))
        self.canvas.fill(colors.light_blue)
        pygame.display.update()

        #self.painter = Painter(self)

        self.camera = Point3D(0, 0, 0)
        self.d = 200

        self.lights = []
        self.lights.append(LightSource(position=Point3D(5, 5, 5), color=colors.white, directional_intensity=255, ambient_intensity=100))
        self.lights.append(LightSource(position=Point3D(5, 5, 5), color=colors.red, directional_intensity=255, ambient_intensity=100))
        self.lights.append(LightSource(position=Point3D(5, 5, 5), color=colors.green, directional_intensity=255, ambient_intensity=100))
        self.lights.append(LightSource(position=Point3D(5, 5, 5), color=colors.blue, directional_intensity=255, ambient_intensity=100))
        self.light = self.lights[0]

        self.shapes = []
        self.materials = []
        self.materials.append(Material(k_a=0, k_d=0.5, k_s=0.5, n=50, color=colors.light_blue))
        self.materials.append(Material(k_a=0, k_d=0.5, k_s=0.5, n=50, color=colors.red))
        self.materials.append(Material(k_a=0, k_d=0.5, k_s=0.5, n=50, color=colors.violet))
        self.materials.append(Material(k_a=0, k_d=0.2, k_s=0.8, n=50, color=colors.black))
        self.materials.append(Material(k_a=0, k_d=0.8, k_s=0.2, n=50, color=colors.black))

        self.materials.append(Material(k_a=0, k_d=0.5, k_s=0.5, n=10, color=colors.black))
        self.materials.append(Material(k_a=0, k_d=0.5, k_s=0.5, n=200, color=colors.black))

        self.materials.append(Material(k_a=0, k_d=0.8, k_s=0.2, n=2, color=colors.black))

        self.initialize()
        self.draw()

    def initialize(self):
        self.shapes.append(Sphere(Point3D(0, 0, 20), 10, self.materials[0]))

    def draw(self):
        self.canvas.fill(colors.light_blue)
        for shape in self.shapes:
            shape.draw(self)
        self.light.draw(self)

    def handle_move(self, event):
        handler = {
            'w': lambda: self.move(self.move_step, Axis.Y),
            's': lambda: self.move(-self.move_step, Axis.Y),
            'a': lambda: self.move(self.move_step, Axis.X),
            'd': lambda: self.move(-self.move_step, Axis.X),
            'e': lambda: self.move(-self.move_step, Axis.Z),
            'q': lambda: self.move(self.move_step, Axis.Z)
        }.get(event['keysym'])

        if handler:
            handler()
            self.draw()

    def move(self, distance, axis):
        matrix = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]], dtype=float)

        matrix[axis.value, 3] = distance

        for shape in self.shapes:
            shape.transform(matrix)
        self.light.transform(matrix)

    def handle_turn(self, event):
        handler = {
            'w': lambda: self.rotate(self.rotate_step, Axis.X),
            's': lambda: self.rotate(-self.rotate_step, Axis.X),
            'a': lambda: self.rotate(-self.rotate_step, Axis.Y),
            'd': lambda: self.rotate(self.rotate_step, Axis.Y),
            'e': lambda: self.rotate(-self.rotate_step, Axis.Z),
            'q': lambda: self.rotate(self.rotate_step, Axis.Z)
        }.get(event['keysym'])

        if handler:
            handler()
            self.draw()

    def rotate(self, angle, axis):
        matrix = np.array([[1, 0, 0, 0],
                           [0, 1, 0, 0],
                           [0, 0, 1, 0],
                           [0, 0, 0, 1]], dtype=float)

        if axis == Axis.X:
            matrix[1:3, 1:3] = np.array([[cos(angle), -sin(angle)],
                                         [sin(angle), cos(angle)]])
        elif axis == Axis.Y:
            matrix[0:3, 0:3] = np.array([[cos(angle), 0, sin(angle)],
                                         [0, 1, 0],
                                         [-sin(angle), 0, cos(angle)]])
        elif axis == Axis.Z:
            matrix[0:2, 0:2] = np.array([[cos(angle), -sin(angle)],
                                         [sin(angle), cos(angle)]])

        for shape in self.shapes:
            shape.transform(matrix)
        self.light.transform(matrix)

    def handle_zoom(self, event):
        if event['keysym'] == '+':
            self.d += self.zoom_step
        elif event['keysym'] == '-':
            self.d -= self.zoom_step
        self.draw()

    def handle_material_change(self, event):
        handler = {
            '1': lambda: self.change_material(0),
            '2': lambda: self.change_material(1),
            '3': lambda: self.change_material(2),
            '4': lambda: self.change_material(3),
            '5': lambda: self.change_material(4),
            '6': lambda: self.change_material(5),
            '7': lambda: self.change_material(6),
            '8': lambda: self.change_material(7),
            '9': lambda: self.change_material(8),
            '0': lambda: self.change_material(9)
        }.get(event['keysym'])

        if handler:
            handler()
            self.draw()

    def change_material(self, index):
        if index < len(self.materials):
            self.shapes[0].material = self.materials[index]

    def handle_light_change(self, event):
        handler = {
            '1': lambda: self.change_light(0),
            '2': lambda: self.change_light(1),
            '3': lambda: self.change_light(2),
            '4': lambda: self.change_light(3),
            '5': lambda: self.change_light(4),
            '6': lambda: self.change_light(5),
            '7': lambda: self.change_light(6),
            '8': lambda: self.change_light(7),
            '9': lambda: self.change_light(8),
            '0': lambda: self.change_light(9)
        }.get(event['keysym'])

        if handler:
            handler()
            self.draw()

    def change_light(self, index):
        if index < len(self.lights):
            self.light = self.lights[index]

    def reset(self):
        self.d = 200
        self.shapes = []
        self.initialize()

        self.draw()
