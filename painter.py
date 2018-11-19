class Painter(object):
    def __init__(self, scene):
        self.scene = scene

    def draw(self):
        faces = self.split_faces()
        print(faces)
        faces.sort(key=self.distance_from_camera, reverse=True)
        for face in faces:
            face.draw(self.scene)

    def distance_from_camera(self, face):
        return face.distance_from_camera(self.scene)

    def split_faces(self):
        split_faces = []
        for shape in self.scene.shapes:
            for face in shape.faces:
                split_faces.extend(face.split())
        return split_faces
