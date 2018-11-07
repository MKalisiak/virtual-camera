from point import Point3D
from ordered_set import OrderedSet


class Edge(object):
    def __init__(self, start_point, end_point):
        self.start_point = start_point
        self.end_point = end_point


class Face(object):
    def __init__(self, edges: [Edge]):
        self.edges = edges
        self.gravity_center = self.calc_gravity_center()

    def calc_gravity_center(self):
        center = Point3D(0, 0, 0)
        for point in self.unique_points():
            center = center.add_point(point)
        return center.divide_by_scalar(len(self.unique_points()))

    def unique_points(self):
        points = []
        for edge in self.edges:
            points.append(edge.start_point)
            points.append(edge.end_point)
        return list(OrderedSet(points))

    def draw(self, scene):
        #TODO dont draw if behind camera
        scene.canvas.create_polygon(self.flat_points(scene), outline="white", fill="blue")

        # for edge in self.edges:
        #     if edge.start_point.z <= 0 or edge.end_point.z <= 0:
        #         continue
        #     projected_start = edge.start_point.project(scene)
        #     projected_end = edge.end_point.project(scene)
        #     scene.canvas.create_line(projected_start.x, projected_start.y,
        #                              projected_end.x, projected_end.y,
        #                              fill="white")

    def flat_points(self, scene):
        points = []
        for point in self.unique_points():
            points.append(point.project(scene).x)
            points.append(point.project(scene).y)
        return points


class Cuboid(object):
    def __init__(self, start_point, width, depth, height, color):
        self.color = color
        p = start_point
        self.bottom_0 = Point3D(p.x, p.y, p.z)
        self.bottom_1 = Point3D(p.x + width, p.y, p.z)
        self.bottom_2 = Point3D(p.x + width, p.y, p.z + depth)
        self.bottom_3 = Point3D(p.x, p.y, p.z + depth)

        self.top_0 = Point3D(p.x, p.y + height, p.z)
        self.top_1 = Point3D(p.x + width, p.y + height, p.z)
        self.top_2 = Point3D(p.x + width, p.y + height, p.z + depth)
        self.top_3 = Point3D(p.x, p.y + height, p.z + depth)

        self.edge_bottom_0 = Edge(self.bottom_0, self.bottom_1)
        self.edge_bottom_1 = Edge(self.bottom_1, self.bottom_2)
        self.edge_bottom_2 = Edge(self.bottom_2, self.bottom_3)
        self.edge_bottom_3 = Edge(self.bottom_3, self.bottom_0)
        self.edge_vertical_0 = Edge(self.bottom_0, self.top_0)
        self.edge_vertical_1 = Edge(self.bottom_1, self.top_1)
        self.edge_vertical_2 = Edge(self.bottom_2, self.top_2)
        self.edge_vertical_3 = Edge(self.bottom_3, self.top_3)
        self.edge_top_0 = Edge(self.top_0, self.top_1)
        self.edge_top_1 = Edge(self.top_1, self.top_2)
        self.edge_top_2 = Edge(self.top_2, self.top_3)
        self.edge_top_3 = Edge(self.top_3, self.top_0)

        self.points = [self.bottom_0, self.bottom_1, self.bottom_2, self.bottom_3,
                       self.top_0, self.top_1, self.top_2, self.top_3]

        self.edges = [
            self.edge_bottom_0,
            self.edge_bottom_1,
            self.edge_bottom_2,
            self.edge_bottom_3,
            self.edge_vertical_0,
            self.edge_vertical_1,
            self.edge_vertical_2,
            self.edge_vertical_3,
            self.edge_top_0,
            self.edge_top_1,
            self.edge_top_2,
            self.edge_top_3
        ]

        self.faces = [
            Face([self.edge_bottom_0, self.edge_bottom_1, self.edge_bottom_2, self.edge_bottom_3]),
            Face([self.edge_top_0, self.edge_top_1, self.edge_top_2, self.edge_top_3]),
            Face([self.edge_bottom_0, self.edge_vertical_1, self.edge_top_0, self.edge_vertical_0]),
            Face([self.edge_bottom_1, self.edge_vertical_2, self.edge_top_1, self.edge_vertical_1]),
            Face([self.edge_bottom_2, self.edge_vertical_3, self.edge_top_2, self.edge_vertical_2]),
            Face([self.edge_bottom_3, self.edge_vertical_0, self.edge_top_3, self.edge_vertical_3])
        ]


    def transform(self, matrix):
        for point in self.points:
            point.transform(matrix)






