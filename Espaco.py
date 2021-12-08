from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr

def cubo(VAO, VBO, cubo_buffer, EBO, cubo_indices):
    # cubo VAO
    glBindVertexArray(VAO)
    # cubo Vértice Buffer Objeto
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, cubo_buffer.nbytes, cubo_buffer, GL_STATIC_DRAW)

    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, cubo_indices.nbytes, cubo_indices, GL_STATIC_DRAW)

    # cubo vértices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, cubo_buffer.itemsize * 8, ctypes.c_void_p(0))
    # cubo texturas
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, cubo_buffer.itemsize * 8, ctypes.c_void_p(12))
    # cubo normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, cubo_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)


def sala(VAO, VBO, sala_buffer):
    # VAO
    glBindVertexArray(VAO)
    # Vértice Buffer Objeto
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, sala_buffer.nbytes, sala_buffer, GL_STATIC_DRAW)

    # vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sala_buffer.itemsize * 8, ctypes.c_void_p(0))
    # texturas
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sala_buffer.itemsize * 8, ctypes.c_void_p(12))
    # normais
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, sala_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)
