class Painter(object):
    def __init__(self, scene):
        self.scene = scene

    def draw(self):
        faces = []
        for shape in self.scene.shapes:
            for face in shape.faces:
                faces.append(face)
        faces.sort(key=self.distance_from_camera, reverse=True)
        for face in faces:
            face.draw(self.scene)

    def distance_from_camera(self, face):
        return face.distance_from_camera(self.scene)
