from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import glfw

vertices = [
    [-0.1, 0.0],
    [-0.25, 0.3],
    [-.3, 0.25],
    [0.5, 0.9],
    [0.66666, -0.25],
    [-0.25, -0.25],
    [-.3, .3]
]

colors = [
    [1.0, 0.1, 0.0],
    [0.0, 1.1, 0.0],
    [0.0, 0.1, 1.0],
    [1.0, 1.1, 0.0],
    [1.0, 0.1, 1.0],
    [0.0, 1.1, 1.0]
]

angle = 0
color_index = 0

def draw_polygon():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    glPushMatrix()
    glRotatef(angle, 0.0, 0.0, 1.0)
    glBegin(GL_POLYGON)
    for i in range(len(vertices)):
        glColor3f(*colors[(color_index + i) % len(colors)])
        glVertex2f(*vertices[i])
    glEnd()

    glPopMatrix()
    glutSwapBuffers()

def key_pressed(key, x, y):
    global color_index
    if key == b' ':
        glutTimerFunc(30, update_scene, 0)

def update_scene(value):
    global angle
    angle += 2
    if angle > 360:
        angle -= 360
    glutPostRedisplay()
    glutTimerFunc(30, update_scene, 0)

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(720, 720)
glutCreateWindow("lab1")
glutDisplayFunc(draw_polygon)
glutKeyboardFunc(key_pressed)
glClearColor(0.0, 0.0, 0.0, 1.0)
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(-1.0, 1.0, -1.0, 1.0, -1.0, 1.0)
glutTimerFunc(30, update_scene, 0)
glutMainLoop()
