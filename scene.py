import tkinter as tk
import math
from cuboid import Cuboid
from point import Point


class Scene(object):
    def __init__(self, master):
        self.width = 800
        self.height = 800
        self.move_step = 2
        self.zoom_step = 5
        self.rotate_step = math.pi / 18
        self.canvas = tk.Canvas(master, width=self.width, height=self.height, bg="black")
        self.canvas.pack()

        self.d = 200

        self.shapes = []
        self.initialize()
        self.draw()

    def initialize(self):
        self.shapes.append(Cuboid(Point(2, -5, 20), 10, 10, 10))
        self.shapes.append(Cuboid(Point(-12, -5, 20), 10, 10, 10))
        self.shapes.append(Cuboid(Point(2, -5, 32), 10, 10, 10))
        self.shapes.append(Cuboid(Point(-12, -5, 32), 10, 10, 10))

    def draw(self):
        self.canvas.delete(tk.ALL)
        for shape in self.shapes:
            shape.draw(self)

    def handle_move(self, event):
        handler = {
            'w': lambda: self.move(self.move_step, 1),
            's': lambda: self.move(-self.move_step, 1),
            'a': lambda: self.move(self.move_step, 0),
            'd': lambda: self.move(-self.move_step, 0),
            'e': lambda: self.move(-self.move_step, 2),
            'q': lambda: self.move(self.move_step, 2)
        }.get(event.keysym)

        if handler:
            handler()
            self.draw()

    def move(self, distance, axis):
        for shape in self.shapes:
            shape.translate(distance, axis)

    def handle_turn(self, event):
        handler = {
            'w': lambda: self.rotate(self.rotate_step, 0),
            's': lambda: self.rotate(-self.rotate_step, 0),
            'a': lambda: self.rotate(-self.rotate_step, 1),
            'd': lambda: self.rotate(self.rotate_step, 1),
            'e': lambda: self.rotate(-self.rotate_step, 2),
            'q': lambda: self.rotate(self.rotate_step, 2)
        }.get(event.keysym)

        if handler:
            handler()
            self.draw()

    def rotate(self, angle, axis):
        for shape in self.shapes:
            shape.rotate(angle, axis)

    def handle_zoom(self, event):
        if event.delta > 0:
            self.d += self.zoom_step
        else:
            self.d -= self.zoom_step
        self.draw()

    def reset(self, event):
        self.d = 200
        self.shapes = []
        self.initialize()

        self.draw()
