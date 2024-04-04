from time import sleep
import numpy as np
import glfw
from OpenGL.GL import *

a = np.pi / 2
l = .25
T = (1, 0, 0, 0,
     0, 1, 0, 0,
     0, 0, 1, 0,
     0, 0, 0, 1)

sizeX = 1024
sizeY = 720
data = [[255] * sizeX for i in range(sizeY)]
points = []
confluence = [0] * sizeY


def filtration():
    global data
    mask = [[1, 2, 1],
            [2, 4, 2],
            [1, 2, 1]]
    for i in range(1, sizeY - 1):
        for j in range(1, sizeX - 1):
            if zeroChek(data, i, j):
                data[i][j] = int(
                    (mask[0][0] * data[i + 1][j - 1] + mask[0][1] * data[i + 1][j] + mask[0][2] * data[i + 1][j + 1] +
                     mask[1][0] * data[i][j - 1]   +   mask[1][1] * data[i][j]   +   mask[1][2] * data[i][j + 1] +
                     mask[2][0] * data[i - 1][j - 1] + mask[2][1] * data[i - 1][j] + mask[2][2] * data[i - 1][j + 1])
                    / 16)
            else:
                data[i][j] = 0


def zeroChek(data, i, j):
    return 0 < (data[i + 1][j - 1] + data[i + 1][j] + data[i + 1][j + 1] + data[i][j - 1] + data[i][j] + data[i][j + 1]
                + data[i - 1][j - 1] + data[i - 1][j] + data[i - 1][j + 1])


def fill():
    Oy = []
    Ox = []
    for point_x, point_y in points:
        Oy.append(point_x)
        Ox.append(point_y)
    for i in range(sizeY):
        isInside = False
        j = 0
        black = data[i].count(0)
        if black == 1:
            continue
        while j < sizeX - 2:
            if data[i][j + 1] == 0 and not isInside:
                isInside = True
                d = 0
                while data[i][j + 1] == 0:
                    if not (0 in data[i][j + 1:]):
                        break
                    d += 1
                    j += 1
                if not (0 in data[i][j + 1:]):
                    break
            elif data[i][j + 1] == 0 and isInside:
                isInside = False
                d = 0
                while data[i][j + 1] == 0:
                    d += 1
                    j += 1
                cond = d < 3 and (j in Ox)
                if (0 in data[i][j + 1:]) and (0 in data[i][0:j]) and ([j, i] in points or cond):
                    isInside = True
            if isInside:
                data[i][j + 1] = 128
            else:
                data[i][j + 1] = 255
            j += 1


def drawLine(x0, y0, x1, y1):
    global confluence
    if x0 == x1:
        m = 2 ** 32
    else:
        m = ((y1 - y0) /
             (x1 - x0))
    e = -.5
    x = x0
    y = y0
    isSharp = True
    if x <= x1 and y <= y1:
        if m > 1:
            isSharp = False
            m **= -1
        while x <= x1 and y <= y1:
            data[y][x] = 0
            if isSharp:
                x += 1
            else:
                confluence[y] += 1
                y += 1
            e += m
            if e >= 0:
                if isSharp:
                    confluence[y] += 1
                    y += 1
                else:
                    x += 1
                e -= 1
    elif x >= x1 and y <= y1:
        m = -m
        if m > 1:
            isSharp = False
            m **= -1
        while x >= x1 and y <= y1:
            data[y][x] = 0
            if isSharp:
                x -= 1
            else:
                confluence[y] += 1
                y += 1
            e += m
            if e >= 0:
                if isSharp:
                    confluence[y] += 1
                    y += 1
                else:
                    x -= 1
                e -= 1
    elif x >= x1 and y >= y1:
        if m > 1:
            isSharp = False
            m **= -1
        while x >= x1 and y >= y1:
            data[y][x] = 0
            if isSharp:
                x -= 1
            else:
                confluence[y] += 1
                y -= 1
            e += m
            if e >= 0:
                if isSharp:
                    confluence[y] += 1
                    y -= 1
                else:
                    x -= 1
                e -= 1
    elif x <= x1 and y >= y1:
        m = -m
        if m > 1:
            m **= -1
            isSharp = False
        while x <= x1 and y >= y1:
            data[y][x] = 0
            if isSharp:
                x += 1
            else:
                confluence[y] += 1
                y -= 1
            e += m
            if e >= 0:
                if isSharp:
                    confluence[y] += 1
                    y -= 1
                else:
                    x += 1
                e -= 1


def display(window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glClearColor(0, 0, 0, 0)
    glRasterPos(-1, -1)
    glPixelZoom(2, 2)
    glDrawPixels(1024, 720, GL_GREEN, GL_UNSIGNED_BYTE, data)
    glfw.swap_buffers(window)
    glfw.poll_events()


def mouse_button_callback(window, button, action, mods):
    global points
    if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
        t = list(glfw.get_cursor_pos(window))
        t[0] = int(t[0] - 128)
        t[1] = int(700 - t[1] - 96)
        print(f"Ox = {t[0]}, Oy = {t[1]}")
        if len(points) > 0:
            drawLine(points[-1][0], points[-1][1], t[0], t[1])
            confluence[points[-1][1]] -= 1
        points.append(t)


def key_callback(window, key, scancode, action, mods):
    global data
    if key == glfw.KEY_SPACE and action == glfw.PRESS:
        drawLine(points[-1][0], points[-1][1], points[0][0], points[0][1])
        confluence[points[0][1]] -= 1
        confluence[points[-1][1]] -= 1
    if key == glfw.KEY_1 and action == glfw.PRESS:
        fill()
    if key == glfw.KEY_2 and action == glfw.PRESS:
        filtration()
    


def scroll_callback(window, xoffset, yoffset):
    global size
    if xoffset > 0:
        size -= yoffset / 10
    else:
        size += yoffset / 10


def main():
    if not glfw.init():
        return
    window = glfw.create_window(1024, 720, "lab4", None, None)
    if not window:
        glfw.terminate()
        return
    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    while not glfw.window_should_close(window):
        display(window)
    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == '__main__':
    main()
