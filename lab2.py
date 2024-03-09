from OpenGL.GLUT import *
from OpenGL.GL import *
import numpy as np

# from pyopengl.OpenGL.raw.GL.VERSION.GL_1_0 import glFrustum

a = np.pi/2
l = .25
TT = (1, 0, -l * np.cos(a), 0 ,
    0, 1, -l * np.sin(a), 0,
    0, 0, -1, 0,
    0, 0, 0, 1)

T = (1, 0, 0, 0 ,
    0, 1, 0, 0,
    -l * np.cos(a), -l * np.sin(a), -1, 0,
    0, 0, 0, 1)

size = 1

def init():
    glClearColor(0, 0, 0, 0)
    glShadeModel(GL_FLAT)

def display():
    # glMatrixMode(GL_PROJECTION)
    # glLoadIdentity()

    n = (1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, -1, 0,
         1, -1, -3, 1)

    glMultMatrixd(n)

    glClear(GL_COLOR_BUFFER_BIT)

    glMultMatrixd(T)

    glBegin(GL_QUADS)

    glColor3f(1, 0, 0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)

    glColor3f(0, 1, 0)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)

    glColor3f(0, 0, 1)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)

    glColor3f(1, 0, 1)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)

    glColor3f(1, 1, 0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)

    glColor3f(0, 1, 1)
    glVertex3f(-size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)

    glEnd()
    #________________________________________________________
    glLoadIdentity()
    n = (1, 0, 0, 0,
         0, 1, 0, 0,
         0, 0, 1, 0,
         1, 1, -3, 1)
    glMultMatrixd(n)



    glBegin(GL_QUADS)
    glColor3f(1, 0, 0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)

    glColor3f(0, 1, 0)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)

    glColor3f(0, 0, 1)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(-size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)

    glColor3f(1, 0, 1)
    glVertex3f(-size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)

    glColor3f(1, 1, 0)
    glVertex3f(-size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, -size / 2, -size / 2)
    glVertex3f(size / 2, size / 2, -size / 2)
    glVertex3f(-size / 2, size / 2, -size / 2)

    glColor3f(0, 1, 1)
    glVertex3f(-size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, -size / 2, size / 2)
    glVertex3f(size / 2, size / 2, size / 2)
    glVertex3f(-size / 2, size / 2, size / 2)

    glEnd()
    glColor3f(1, 1, 1)
    glLoadIdentity()


    glFlush()


def reshape( w, h ):
    glViewport(0, 0, w, h)
    glMatrixMode(GL_PROJECTION)


    glFrustum(-1, 1, -1, 1, 1.5, 20)
    glMatrixMode(GL_MODELVIEW)

def keyboard(key, x, y):
    global a, b, T,  l
    if key == b's':
        a -= np.pi / 12
        # l +=0.75
        # T = (1, 0, 0, 0,
        #      0, 1, 0, 0,
        #      np.cos(a), np.sin(a), -1, 0,
        #      0, 0, 0, 1)
        T = (1, 0, 0, 0,
            0, 1, 0, 0,
            np.cos(a), np.sin(a), -1, 0,
            0, 0, 0, 1)
    if key == b'w':
        a += np.pi / 12
        # l +=0.75
        T = (1, 0, -l * np.cos(a), 0,
             0, 1, -l * np.sin(a), 0,
             0, 0, -1, 0,
             0, 0, 0, 1)


    if key == b'1':
        a -= np.pi / 12

        l += 0.75
        a = np.pi

        T = (1, 0, 0, 0,
             0, 1, 0, 0,
             np.cos(a), np.sin(a), -1, 0,
             0, 0, 0, 1)

    glutPostRedisplay()

def main():
    global a
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutInitWindowSize(500, 500)
    glutInitWindowPosition(100, 100)
    glutCreateWindow(b'cube')
    init()
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glutKeyboardFunc(keyboard)
    glutMainLoop()


if __name__ == "__main__":
    main()
