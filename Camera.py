from pyrr import Vector3, vector, vector3, matrix44
from math import sin, cos, radians

class Camera:
    def __init__(self):
        self.camera_pos = Vector3([0.0, 4.0, 3.0])
        self.camera_frente = Vector3([0.0, 0.0, -1.0])
        self.camera_cima = Vector3([0.0, 1.0, 0.0])
        self.camera_direita = Vector3([1.0, 0.0, 0.0])

        self.mouse_sen = 0.25
        self.jaw = -90 # se move no eixo x, ao redor do objeto
        self.pitch = 0 # movimento da camera para cima e para baixo, eixo y

    def get_view_matrix(self):
        # Cria uma olhada na matriz de acordo com os padrões do OpenGL.
        return matrix44.create_look_at(self.camera_pos, self.camera_pos + self.camera_frente, self.camera_cima)

    def processar_mouse_movemento(self, xoffset, yoffset, constrain_pitch=True):
        xoffset *= self.mouse_sen
        yoffset *= self.mouse_sen

        self.jaw += xoffset
        self.pitch += yoffset

        # soma e arredonda os angulos do mouse
        if constrain_pitch:
            if self.pitch > 45:
                self.pitch = 45
            if self.pitch < -45:
                self.pitch = -45

        self.att_camera_vectors()


    def att_camera_vectors(self):
        frente = Vector3([0.0, 0.0, 0.0])
        frente.x = cos(radians(self.jaw)) * cos(radians(self.pitch))
        frente.y = sin(radians(self.pitch))
        frente.z = sin(radians(self.jaw)) * cos(radians(self.pitch))

        self.camera_frente = vector.normalise(frente)
        self.camera_direita = vector.normalise(vector3.cross(self.camera_frente, Vector3([0.0, 1.0, 0.0])))
        self.camera_cima = vector.normalise(vector3.cross(self.camera_direita, self.camera_frente))

    # Camera meotodo para WASD movimento
    def processar_teclado(self, direcao, velocidade):
        if direcao == "PFRENTE":
            self.camera_pos += self.camera_frente * velocidade
        if direcao == "PTRAS":
            self.camera_pos -= self.camera_frente * velocidade
        if direcao == "ESQUERDA":
            self.camera_pos -= self.camera_direita * velocidade
        if direcao == "DIREITA":
            self.camera_pos += self.camera_direita * velocidade
