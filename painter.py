class Painter(object):
    def __init__(self, scene):
        self.scene = scene

    def draw(self):
        faces = []
        for shape in self.scene.shapes:
            for face in shape.faces:
                faces.append(face)
        faces.sort(key=lambda face: face.calc_gravity_center().x **2 + face.calc_gravity_center().y ** 2 + face.calc_gravity_center().z ** 2  , reverse=True)
        for face in faces:
            face.draw(self.scene)

