from CriarCena import *
from Camera import Camera
import pygame

cam = Camera()
mouse = True

# receve as novas posições do mouse e atualiza na tela
def cam_mouse(x_pos, y_pos):
    global mouse, x_ant, y_ant

    if mouse:
        x_ant = x_pos
        y_ant = y_pos
        mouse = False

    xoffset = x_pos - x_ant
    yoffset = y_ant - y_pos

    x_ant = x_pos
    y_ant = y_pos

    cam.processar_mouse_movemento(xoffset, yoffset)

def configura_teclas_movimento():

    # Define as teclas para se movimentar
    tecla_pressionada = pygame.key.get_pressed()
    if tecla_pressionada[pygame.K_a]:
        cam.processar_teclado("ESQUERDA", 0.06)
    if tecla_pressionada[pygame.K_d]:
        cam.processar_teclado("DIREITA", 0.06)
    if tecla_pressionada[pygame.K_w]:
        cam.processar_teclado("PFRENTE", 0.06)
    if tecla_pressionada[pygame.K_s]:
        cam.processar_teclado("PTRAS", 0.06)

def configura_mouse():

        mouse_pos = pygame.mouse.get_pos()
        cam_mouse(mouse_pos[0], mouse_pos[1])

        # Para que consiga uma visão de 360 graus
        if mouse_pos[0] <= 0:
            pygame.mouse.set_pos((1279, mouse_pos[1]))
        elif mouse_pos[0] >= 1279:
            pygame.mouse.set_pos((0, mouse_pos[1]))
