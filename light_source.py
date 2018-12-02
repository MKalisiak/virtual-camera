from point import Point3D
import colors
import pygame


class LightSource(object):
    def __init__(self, position: Point3D, color):
        self.position = position
        self.color = color

    def draw(self, scene):
        if self.position.z <= 0:
            return

        projected_center = self.position.project(scene)

        projected_center = (int(projected_center.x), int(projected_center.y))

        pygame.draw.circle(scene.canvas, colors.white, projected_center, 1, 0)

    def transform(self, matrix):
        self.position.transform(matrix)
