from Movimento import *
from Espaco import *
from Camera import Camera
from CarregarObj import CarregarObj
from CarregarTextura import carregar_textura_pygame
import pyrr
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL import *
import pygame
import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'


LARGURA, ALTURA = 1280, 720
lastX, lastY = LARGURA / 2, ALTURA / 2

vertex_src = """
# version 330
layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;
uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;
out vec2 v_texture;
void main()
{
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
}
"""

fragment_src = """
# version 330
in vec2 v_texture;
out vec4 out_color;
uniform sampler2D s_texture;
void main()
{
    out_color = texture(s_texture, v_texture);
}
"""


def carregar_texturas(caminho, textura):
    carregar_textura_pygame(caminho, textura)


def desenhar_objetos(VAO, textura, indice, posicao, model_loc, GL):

    glBindVertexArray(VAO)
    glBindTexture(GL_TEXTURE_2D, textura)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, posicao)
    glDrawArrays(GL, 0, len(indice))


def desenhar_cubo(cubo_pos, cubo_indices, VAO, textura, ct, model_loc):

    #rotação dos cubos
    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * ct)
    model = pyrr.matrix44.multiply(rot_y, cubo_pos)

    # desenhar cubo
    glBindVertexArray(VAO)
    glBindTexture(GL_TEXTURE_2D, textura)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawElements(GL_TRIANGLES, len(cubo_indices), GL_UNSIGNED_INT, None)


def criar():

    pygame.init()
    pygame.display.set_mode((LARGURA, ALTURA), pygame.OPENGL |
                            pygame.DOUBLEBUF | pygame.RESIZABLE)  # |pygame.FULLSCREEN
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    # carregando os meshes
    cubo_indices, cubo_buffer = CarregarObj.carregar_model("meshes/cubos/cubo.obj", False)
    sala_indices, sala_buffer = CarregarObj.carregar_model("meshes/chao/chao.obj")
    banco_indices, banco_buffer = CarregarObj.carregar_model("meshes/banco/banco.obj")
    mulher_indices, mulher_buffer = CarregarObj.carregar_model("meshes/mulher_sentada/mulher_sentada.obj")
    nave_indices, nave_buffer = CarregarObj.carregar_model("meshes/nave/nave.obj")
    quadro1_indices, quadro1_buffer = CarregarObj.carregar_model("meshes/quadro/quadro.obj")
    quadro2_indices, quadro2_buffer = CarregarObj.carregar_model("meshes/quadro/quadro2.obj")
    flame_indices, flame_buffer = CarregarObj.carregar_model("meshes/objetos extras/fogo.obj")

    shader = compileProgram(compileShader(
        vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    # VAO e VBO
    VAO = glGenVertexArrays(12)
    VBO = glGenBuffers(12)
    EBO = glGenBuffers(1)
    texturas = glGenTextures(12)

    sala(VAO[0], VBO[0], sala_buffer)
    sala(VAO[1], VBO[1], sala_buffer)
    sala(VAO[6], VBO[6], banco_buffer)
    sala(VAO[2], VBO[2], mulher_buffer)
    sala(VAO[7], VBO[7], nave_buffer)
    sala(VAO[8], VBO[8], quadro1_buffer)
    sala(VAO[9], VBO[9], quadro1_buffer)
    sala(VAO[11], VBO[11], flame_buffer)

    cubo(VAO[3], VBO[3], cubo_buffer, EBO, cubo_indices)
    cubo(VAO[4], VBO[4], cubo_buffer, EBO, cubo_indices)
    cubo(VAO[5], VBO[5], cubo_buffer, EBO, cubo_indices)

    carregar_texturas("meshes/chao/chao.jpg", texturas[0])
    carregar_texturas("meshes/texturas_auxiliar/teto_estrelado.jpg", texturas[1])
    carregar_texturas("meshes/mulher_sentada/mulher_sentada.jpg", texturas[2])
    carregar_texturas("meshes/cubos/cubo_picasso.png", texturas[3])
    carregar_texturas("meshes/cubos/cubo_vahgogh.png", texturas[4])
    carregar_texturas("meshes/cubos/cubo_davinci.png", texturas[5])
    carregar_texturas("meshes/texturas_auxiliar/wood.jpg", texturas[6])
    carregar_texturas("meshes/nave/ufo_diffuse.png", texturas[7])
    carregar_texturas("meshes/quadro/quadro1.jpg", texturas[8])
    carregar_texturas("meshes/quadro/quadro5.jpg", texturas[9])
    carregar_texturas("meshes/texturas_auxiliar/red.jpg", texturas[11])

    glUseProgram(shader)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
    mulher_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 1.2, -13]))
    chao_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    teto_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 20, 0]))
    cubo_picasso_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-15, 5, -10]))
    cubo_vahgogh_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-13, 5, -15]))
    cubo_davinci_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-10, 7, -8]))
    banco_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0.1, -15]))
    nave_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 19, -15]))
    quadro1_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 6, -15]))
    quadro2_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([10, 6, -15]))
    flame_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-10, 1, 13]))

    model_loc = glGetUniformLocation(shader, "model")
    proj_loc = glGetUniformLocation(shader, "projection")
    view_loc = glGetUniformLocation(shader, "view")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.VIDEORESIZE:
                glViewport(0, 0, event.w, event.h)
                projection = pyrr.matrix44.create_perspective_projection_matrix(
                    45, event.w / event.h, 0.1, 100)
                glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

        configura_teclas_movimento()
        configura_mouse()

        ct = pygame.time.get_ticks() / 1000

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        desenhar_cubo(cubo_picasso_pos, cubo_indices, VAO[3], texturas[3], ct, model_loc)
        desenhar_cubo(cubo_vahgogh_pos, cubo_indices, VAO[4], texturas[4], ct, model_loc)
        desenhar_cubo(cubo_davinci_pos, cubo_indices, VAO[5], texturas[5], ct, model_loc)

        desenhar_objetos(VAO[0], texturas[0], sala_indices,chao_pos, model_loc, GL_TRIANGLES)
        desenhar_objetos(VAO[2], texturas[2], mulher_indices,mulher_pos, model_loc, GL_TRIANGLES)
        desenhar_objetos(VAO[1], texturas[1], sala_indices,teto_pos, model_loc, GL_TRIANGLES)
        desenhar_objetos(VAO[6], texturas[6], banco_indices,banco_pos, model_loc, GL_TRIANGLES)
        desenhar_objetos(VAO[7], texturas[7], nave_indices,nave_pos, model_loc, GL_TRIANGLES)
        desenhar_objetos(VAO[8], texturas[8], quadro1_indices,quadro1_pos, model_loc, GL_TRIANGLES)
        desenhar_objetos(VAO[9], texturas[9], quadro2_indices,quadro2_pos, model_loc, GL_TRIANGLES)
        desenhar_objetos(VAO[11], texturas[11], flame_indices,flame_pos, model_loc, GL_TRIANGLES)

        pygame.display.flip()
