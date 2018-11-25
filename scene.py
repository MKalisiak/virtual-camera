import math
from cuboid import Cuboid
from point import Point3D
from math import sin, cos
import numpy as np
from axis import Axis
from painter import Painter
import pygame
import colors


class Scene(object):
    def __init__(self):
        self.width = 800
        self.height = 800
        self.move_step = 2
        self.zoom_step = 10
        self.rotate_step = math.pi / 18

        self.canvas = pygame.display.set_mode((self.width, self.height))
        self.canvas.fill(colors.black)
        pygame.display.update()

        self.painter = Painter(self)

        self.camera = Point3D(0, 0, 0)
        self.d = 200

        self.shapes = []
        self.initialize()
        self.draw()

    def initialize(self):
        self.shapes.append(Cuboid(Point3D(2, -5, 20), 10, 10, 10, "red"))
        self.shapes.append(Cuboid(Point3D(-12, -5, 20), 10, 10, 10, "blue"))
        self.shapes.append(Cuboid(Point3D(2, -5, 32), 10, 10, 10, "green"))
        self.shapes.append(Cuboid(Point3D(-12, -5, 32), 10, 10, 10, "yellow"))

    def draw(self):
        self.canvas.fill(colors.black)
        self.painter.draw()

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

    def handle_zoom(self, event):
        if event['keysym'] == '+':
            self.d += self.zoom_step
        elif event['keysym'] == '-':
            self.d -= self.zoom_step
        self.draw()

    def reset(self):
        self.d = 200
        self.shapes = []
        self.initialize()

        self.draw()
