import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame
import time

# Параметры вращения, масштаба и положения камеры
a = np.pi / 2
l = 0.25
T = (1, 0, 0, 0,
     0, 1, 0, 0,
     0, 0, 1, 0,
     0, 0, 0, 1)

# Параметры окна и масштабирования
window_width = 800
window_height = 800
scale = 0.256

# Переменные для управления анимацией
animation_mode = False
texture_sides = None
fi = 0
tetha = 0
sides = 6
radius = 1
height = 1
flying_speed = 0
V = np.pi * 10 ** (-5)
acl = 10 ** (-7)

# Переключатели режимов
light_mode = False
filling_mode = True

# Глобальная переменная для хранения идентификатора дисплейного списка
prism_display_list = None

def create_prism_display_list(cx, cy, cz, r, h, sides):
    """Создает дисплейный список для призмы и возвращает его идентификатор."""
    global prism_display_list
    prism_display_list = glGenLists(1)

    glNewList(prism_display_list, GL_COMPILE)
    glColor3f(1.0, 1.0, 1.0)
    angle_step = 2 * np.pi / sides

    # верхняя грань
    glBegin(GL_POLYGON)
    for i in range(sides):
        angle = i * angle_step
        x = cx + r * np.cos(angle)
        y = cy + r * np.sin(angle)
        glNormal3f(0, 0, 1)
        glTexCoord2f(0.5 + 0.5 * np.cos(angle), 0.5 + 0.5 * np.sin(angle))
        glVertex3f(x, y, cz + h / 2)
    glEnd()

    # нижняя грань
    glBegin(GL_POLYGON)
    for i in range(sides):
        angle = i * angle_step
        x = cx + r * np.cos(angle)
        y = cy + r * np.sin(angle)
        glNormal3f(0, 0, -1)
        glTexCoord2f(0.5 + 0.5 * np.cos(angle), 0.5 + 0.5 * np.sin(angle))
        glVertex3f(x, y, cz - h / 2)
    glEnd()

    # боковые грани
    glBegin(GL_QUAD_STRIP)
    for i in range(sides + 1):
        angle = i * angle_step
        x1 = cx + r * np.cos(angle)
        y1 = cy + r * np.sin(angle)
        x2 = cx + r * np.cos(angle)
        y2 = cy + r * np.sin(angle)

        glNormal3f(np.cos(angle), np.sin(angle), 0)
        glTexCoord2f(i / sides, 0)
        glVertex3f(x1, y1, cz - h / 2)
        glTexCoord2f(i / sides, 1)
        glVertex3f(x2, y2, cz + h / 2)

    glEnd()
    glEndList()

def render_prism(cx, cy, cz, r, h, sides):
    """Отображает призму с использованием дисплейного списка."""
    global prism_display_list
    if prism_display_list is None:
        create_prism_display_list(cx, cy, cz, r, h, sides)
    glCallList(prism_display_list)

def display(window):
    glEnable(GL_DEPTH_TEST)
    glDepthFunc(GL_LESS)
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glLoadIdentity()
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMultMatrixd(T)

    if animation_mode:
        move_object()

    glScale(scale, scale, scale)
    glTranslatef(0, flying_speed, 0)
    glRotatef(fi, 1, 0, 0)
    glRotatef(tetha, 0, 1, 0)

    # Используем дисплейный список для отображения призмы
    render_prism(0, 0, 0, radius, height, sides)

    glfw.swap_buffers(window)
    glfw.poll_events()

def key_callback(window, key, scancode, action, mods):
    global fi, tetha, scale, animation_mode, sides, radius, height, T, a, l

    if key == glfw.KEY_0:
        a -= np.pi / 12
        T = (1, 0, 0, 0,
             0, 1, 0, 0,
             np.cos(a), np.sin(a), 1, 0,
             0, 0, 0, 1)

    if action == glfw.PRESS and key == glfw.KEY_1:
        if sides > 3:
            sides -= 1
            update_prism_display_list()
        else:
            print('Sides must be greater than 3')

    if action == glfw.PRESS and key == glfw.KEY_2:
        sides += 1
        update_prism_display_list()

    if action == glfw.PRESS and key == glfw.KEY_Q:
        if radius > 0.1:
            radius -= 0.1
            update_prism_display_list()
        else:
            print("Radius must be greater than 0.1")

    if action == glfw.PRESS and key == glfw.KEY_E:
        radius += 0.1
        update_prism_display_list()

    if action == glfw.PRESS and key == glfw.KEY_R:
        if height > 0.1:
            height -= 0.1
            update_prism_display_list()
        else:
            print("Height must be greater than 0.1")

    if action == glfw.PRESS and key == glfw.KEY_T:
        height += 0.1
        update_prism_display_list()

    if action == glfw.PRESS and key == glfw.KEY_ENTER:
        mode = glGetIntegerv(GL_POLYGON_MODE)
        if mode[1] == GL_LINE:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_A:
            fi -= 2
        if key == glfw.KEY_D:
            fi += 2
        if key == glfw.KEY_W:
            tetha -= 2
        if key == glfw.KEY_S:
            tetha += 2
        if key == glfw.KEY_UP:
            scale += 0.05
        if key == glfw.KEY_DOWN:
            scale -= 0.05

        global light_mode

        if key == glfw.KEY_L:
            if glIsEnabled(GL_LIGHTING):
                glDisable(GL_LIGHTING)
            else:
                glEnable(GL_LIGHTING)
            return
        if key == glfw.KEY_M:
            animation_mode = not animation_mode
            return

def mouse_callback(window, button, action, mods):
    global filling_mode
    if action == glfw.PRESS:
        if button == glfw.MOUSE_BUTTON_LEFT:
            filling_mode = not filling_mode
            if filling_mode:
                glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            else:
                glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

def move_object():
    global V, flying_speed, acl
    flying_speed -= V
    V += acl
    if flying_speed < -2.2 or flying_speed > 2.2:
        V = -V

def generate_texture():
    textureSurface = pygame.image.load('img_2.png')
    textureData = pygame.image.tobytes(textureSurface, "RGBA")
    width = textureSurface.get_width()
    height = textureSurface.get_height()

    glEnable(GL_TEXTURE_2D)
    texid = glGenTextures(True)

    glBindTexture(GL_TEXTURE_2D, texid)

    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, textureData)

def light():
    glEnable(GL_LIGHTING)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [[0.2, 0.2, 0.2,1]])

    # Light 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0, 0, 0, 1])
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT0, GL_POSITION, [1, 1, -1, 1])
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.2)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.05)

    # Light 1
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0, 0, 0, 1])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.6, 0.6, 0.6, 1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT1, GL_POSITION, [-1, 1, 1, 1])
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.2)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.1)

    # Light 2
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0, 0, 0, 1])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT2, GL_POSITION, [0, -1, 0, 1])
    glLightf(GL_LIGHT2, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT2, GL_LINEAR_ATTENUATION, 0.2)
    glLightf(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.1)

    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1, 1, 1, 1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SHININESS, 50.0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0, 0, 0, 1])

    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)
    glEnable(GL_LIGHT2)

def update_prism_display_list():
    """Обновляет отображаемую призму в дисплейном списке."""
    global prism_display_list
    if prism_display_list is not None:
        glDeleteLists(prism_display_list, 1)
    create_prism_display_list(0, 0, 0, radius, height, sides)

def main():
    if not glfw.init():
        return

    window = glfw.create_window(window_width, window_height, "Prism with Display Lists", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_callback)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    generate_texture()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    light()

    # while not glfw.window_should_close(window):
    #     display(window)
    for _ in range(300):
        display(window)

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == '__main__':
    start = time.monotonic()
    main()
    stop = time.monotonic()
    print('time:', stop - start) # time: 0.625
