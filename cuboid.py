from point import Point3D
from ordered_set import OrderedSet


class Edge(object):
    def __init__(self, start_point : Point3D, end_point : Point3D):
        self.start_point = start_point
        self.end_point = end_point

    def get_middle_point(self):
        return self.start_point.add_point(self.end_point).divide_by_scalar(2)


class Face(object):
    def __init__(self, edges: [Edge]):
        self.edges = edges
        self.gravity_center = self.calc_gravity_center()

    def __repr__(self):
        points = []
        for edge in self.edges:
            points.append(edge.start_point)
            points.append(edge.end_point)
        return  str(points)

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
        if self.is_in_front_of_camera(scene):
            scene.canvas.create_polygon(self.flat_points(scene), outline="white", fill="blue")

    def is_in_front_of_camera(self, scene):
        for edge in self.edges:
            if edge.start_point.z <= scene.camera.z or edge.end_point.z <= scene.camera.z:
                return False
        return True

    def distance_from_camera(self, scene):
        return ((self.gravity_center.x - scene.camera.x) ** 2
                + (self.gravity_center.y - scene.camera.y) ** 2
                + (self.gravity_center.z - scene.camera.z) ** 2)

    def flat_points(self, scene):
        points = []
        for point in self.unique_points():
            points.append(point.project(scene).x)
            points.append(point.project(scene).y)
        return points

    def split(self):
        faces = []
        for index, edge in enumerate(self.edges):
            # edge0 = Edge(edge.start_point, edge.get_middle_point())
            # edge1 = Edge(edge.get_middle_point(),
            #              self.calc_gravity_center())
            # edge2 = Edge(self.calc_gravity_center(),
            #              self.edges[index-1].get_middle_point())
            # edge3 = Edge(self.edges[index-1].get_middle_point(), edge.start_point)
            edge0 = Edge(Point3D(0,0,10), Point3D(10,0,10))
            edge1 = Edge(Point3D(10, 0, 10), Point3D(10, 10, 10))
            edge2 = Edge(Point3D(10, 10, 10), Point3D(0, 10, 10))
            edge3 = Edge(Point3D(0, 10, 10), Point3D(0, 0, 10))


            faces.append(Face([edge0, edge1, edge2, edge3]))
        return faces


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
        for face in self.faces:
            face.gravity_center = face.calc_gravity_center()






