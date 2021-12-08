from CriarCena import *
import pygame

cam = Camera()
mouse = True

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

    cam.process_mouse_movement(xoffset, yoffset)

def configura_teclas_movimento():

    # Define as teclas para se movimentar
    tecla_pressionada = pygame.key.get_pressed()
    if tecla_pressionada[pygame.K_a]:
        cam.process_keyboard("LEFT", 0.02)
    if tecla_pressionada[pygame.K_d]:
        cam.process_keyboard("RIGHT", 0.02)
    if tecla_pressionada[pygame.K_w]:
        cam.process_keyboard("FORWARD", 0.02)
    if tecla_pressionada[pygame.K_s]:
        cam.process_keyboard("BACKWARD", 0.02)

def configura_mouse():

        mouse_pos = pygame.mouse.get_pos()
        cam_mouse(mouse_pos[0], mouse_pos[1])

        # Para que consiga uma visão de 360 graus
        if mouse_pos[0] <= 0:
            pygame.mouse.set_pos((1279, mouse_pos[1]))
        elif mouse_pos[0] >= 1279:
            pygame.mouse.set_pos((0, mouse_pos[1]))
