from OpenGL.GLUT import *
from OpenGL.GL import *
import glfw
from OpenGL.raw.GLU import gluLookAt
import numpy as np
a = np.pi/2
l = .25
degree = 0.0
cnt = 10
T = (1, 0, 0, 0,
    0, 1, 0, 0,
    0, 0, 1, 0,
    0, 0, 0, 1)

def init():
    glClearColor(0.0, 0.0, 0.0, 0.0)
    glShadeModel(GL_FLAT)

def display():
    glLoadIdentity()  # перемещаем в центр СК
    glRotatef(25, 1,2, 0)  # отвечает за поворот
    glClear(GL_COLOR_BUFFER_BIT)

    glScalef(0.6, 0.6, 0.5)  # изменяем мастштаб

    # l = 0.5
    # a = np.pi * 4 / cnt
    # n = (1, 0, 0, 0,
    #      0, 1, 0, 0,
    #      0, 0, 1, 0,
    #      0, 0, 0, 1)

    glRotatef(25, 1,2, 0)  # отвечает за поворот

    l = 0.5
    a = np.pi * 4 / cnt
    n = (1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, 1, 0,
         0, 0, 0, 1)

    glMultMatrixd(n)

    glClear(GL_COLOR_BUFFER_BIT)
    glMultMatrixd(T)

    glBegin(GL_TRIANGLE_FAN)
    glColor3f(0, 0, 0)
    glVertex3f(0, 0, -1)
    for i in range(-1, cnt):
        x = np.sin(a * i) * l
        y = np.cos(a * i) * l
        # glColor3f(0, 40 / 10.0, 1)
        glColor3f(np.random.randint(0, 10), np.random.randint(0, 10), np.random.randint(0, 10))
        glVertex3f(x, y,-1)

    glEnd()
    glVertex3f(0, 0,0)
    glBegin(GL_LINES)
    glColor3f(0, 0, 0)

    for i in range(-1, cnt):
        x = np.sin(a * i) * l
        y = np.cos(a * i) * l
        # glColor3f(1, 0, 0)
        glColor3f(np.random.randint(0, 10), np.random.randint(0, 10), np.random.randint(0, 10))
        glVertex3f(x, y, 0)
        glVertex3f(x, y,-1)

    glEnd()

    glLoadIdentity()

    glRotatef(40, 1,2, 0)  # отвечает за поворот

    glScalef(0.6, 0.6, 0.5)  # изменяем мастштаб

    # glClear(GL_COLOR_BUFFER_BIT)
    glMultMatrixd(T)

    glBegin(GL_TRIANGLE_FAN)
    # glColor3f(np.random.randint(0,255),np.random.randint(0,255), np.random.randint(0,255))
    glVertex3f(0, 0,0)
    for i in range(-1, cnt):
        x = np.sin(a * i) * l
        y = np.cos(a * i) * l
        # glColor3f(0, 2 / 10.0, 1)
        glColor3f(np.random.randint(0, 10), np.random.randint(0, 10), np.random.randint(0, 10))
        glVertex3f(x, y,0)

    glEnd()
    glColor3f(1, 1, 1)
    glLoadIdentity()

    glFlush()


def reshape(w, h):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)
    glFrustum(-1.0, 1.0, -1.0, 1.0, 1.5, 20.0)
    glMatrixMode(GL_MODELVIEW)






def key(key, x, y) :
    global cnt
    global degree
    global a
    global l
    global T

    if (key == b'1'):
        cnt -= 2
    elif (key == b'2'):
        cnt += 2
    if key == b's':
        a -= np.pi / 12

        T = (1, 0, 0, 0,
             0, 1, 0, 0,
             np.cos(a), np.sin(a), 1, 0,
             0, 0, 0, 1)
    if key == b'w':
        a += np.pi / 9
        T = (1, 0, -l * np.cos(a), 0,
             0, 1, -l * np.sin(a), 0,
             0, 0, 1, 0,
             0, 0, 0, 1)

    glutPostRedisplay()

def main():
    global a
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b'lab3')
    init()
    glutDisplayFunc(display)
    # glutReshapeFunc(reshape)
    glutKeyboardFunc(key)
    glutMainLoop()

if __name__ == "__main__":
    main()