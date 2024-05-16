import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GLUT import *
import pygame

a = np.pi / 2
l = .25
T = (1, 0, 0, 0,
     0, 1, 0, 0,
     0, 0, 1, 0,
     0, 0, 0, 1)

window_width = 800
window_height = 800
scale = 0.256

animation_mode = False
texture_sides = None

fi = 0
tetha = 0
sides = 6
radius = 1
height = 1

flying_speed = 0
V = np.pi * 10 ** (-5)
# acl = 0.00006*500
acl = 10 ** (-7)

light_mode = False
filling_mode = True
texture_mode = True

def renderPrism(cx, cy, cz, r, h, sides):
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

    renderPrism(0, 0, 0, radius, height, sides)

    glfw.swap_buffers(window)
    glfw.poll_events()


def key_callback(window, key, scancode, action, mods):
    global x_angle, y_angle, scale, animation_mode, fi, tetha, sides, radius, height, T, a, l

    if key == glfw.KEY_0:
        a -= np.pi / 12

        T = (1, 0, 0, 0,
             0, 1, 0, 0,
             np.cos(a), np.sin(a), 1, 0,
             0, 0, 0, 1)

    if action == glfw.PRESS and key == glfw.KEY_1:
        if sides > 3:
            sides -= 1
        else:
            print('Sides must be greater than 3')

    if action == glfw.PRESS and key == glfw.KEY_2:
        sides += 1

    if action == glfw.PRESS and key == glfw.KEY_Q:
        if radius > 0.1:
            radius -= .1
        else:
            print("Radius must be greater than 0.1")

    if action == glfw.PRESS and key == glfw.KEY_E:
        radius += .1

    if action == glfw.PRESS and key == glfw.KEY_R:
        if height > 0.1:
            height -= .1
        else:
            print("Height must be greater than 0.1")

    if action == glfw.PRESS and key == glfw.KEY_T:
        height += .1

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
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [[0.2, 0.2, 0.2, 1]])

    # Light 0
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0, 0, 0, 1])  # фоновое излучение
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.5, 0.5, 0.5, 1])  # рассеяное излучение
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1])  # зеркальное излучение
    glLightfv(GL_LIGHT0, GL_POSITION, [[1, 1, -1, 1]])  # местоположение источника света
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)  # постоянный коэффициент
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.2)  # линейный коэффициент
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.05)  # квадратичный коэффициент

    # Light 1
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0, 0, 0, 1])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.6, 0.6, 0.6, 1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT1, GL_POSITION, [[-1, 1, 1, 1]])
    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.2)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.1)

    # Light 2
    glLightfv(GL_LIGHT2, GL_AMBIENT, [0, 0, 0, 1])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.8, 0.8, 0.8, 1])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.5, 0.5, 0.5, 1])
    glLightfv(GL_LIGHT2, GL_POSITION, [[0, -1, 0, 1]])
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


def create_shader(shader_type, source):
    shader = glCreateShader(shader_type) # пустой объект шейдера
    glShaderSource(shader, source)# загрузка исходного кода шейдера
    glCompileShader(shader)#компилчция

    # Проверка на ошибки компиляции
    result = glGetShaderiv(shader, GL_COMPILE_STATUS)
    if not result:
        error_log = glGetShaderInfoLog(shader)
        print(f"Error compiling shader type {shader_type}: {error_log}")

    return shader


def main():
    if not glfw.init():
        return

    window = glfw.create_window(window_width, window_height, "lab6", None, None)

    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_key_callback(window, key_callback)
    glfw.set_mouse_button_callback(window, mouse_callback)
    vertex_shader = """
                attribute vec3 aVert; //объявление атрибута вершины aVert, который представляет собой 3D-вектор.
                // объявление varying-переменных
                varying vec3 n; // нормаль 
                varying vec3 v; // вектор от вершины к камере
                varying vec2 uv; //текстурные координаты
                varying vec4 vertexColor; // цвет вершины 
                void main() {   
                    uv = gl_MultiTexCoord0.xy; // присваивание текстурных координат
                    v = vec3(gl_ModelViewMatrix * gl_Vertex); // вычисление вектора от вершины  к камере
                    n = normalize(gl_NormalMatrix * gl_Normal); //  вычисление нормали вершины
                    gl_TexCoord[0] = gl_TextureMatrix[0]  * gl_MultiTexCoord0; // применение текстурной матрицы  к текстурным координатам
                    gl_Position = gl_ModelViewProjectionMatrix * vec4(gl_Vertex.x, gl_Vertex.y, gl_Vertex.z, 1); // вычисление конечной позиции вершины в пространстве отсечения путем умножения матрицы
                    vec4 vertexColor = vec4(0.5f, 0.0f, 0.0f, 1.0f); // присваивание цвета вершины (красный цвет с половинной интенсивностью)
                }
                """

    fragment_shader = """
            varying vec3 n; // Переменная, получающаяся из вершинного шейдера, представляющая нормаль к поверхности в пространстве вида.
            varying vec3 v; // Также получаемая из вершинного шейдера, представляющая вектор от вершины до наблюдателя (камеры).
            varying vec4 vertexColor; //Цвет вершины, передаваемый из вершинного шейдера.

            uniform sampler2D tex; //Текстура, с которой будет взят цвет для текстурирования.
            
            void main () {  
                vec3 L = normalize(gl_LightSource[0].position.xyz - v); // Вектор от поверхности к источнику света
                vec3 E = normalize(-v); // Вектор, направленный к наблюдателю (камере)
                vec3 R = normalize(-reflect(L,n)); // Отраженный вектор света L относительно нормали n.
  
                vec4 Iamb = gl_FrontLightProduct[0].ambient; // Амбиентная составляющая освещения, получаемая из фиксированного функционального набора OpenGL.
                //Диффузное освещение, основанное на косинусе угла между нормалью и направлением к источнику света
                vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(n,L), 1.0); // 
                Idiff = clamp(Idiff, 2.0, 0.6);     
                // Спекулярное освещение, основанное на отраженном векторе R и векторе к наблюдателю E
                vec4 Ispec = gl_LightSource[0].specular 
                                * pow(max(dot(R,E),0.0),0.7); // моделирования блеска (экспоненциальное затухание блеска)
                Ispec = clamp(Ispec, 0.0, 1.0); 

                vec4 texColor = texture2D(tex, gl_TexCoord[0].st); //Цвет текстуры, полученный из текстурного семплера по координатам текстуры
                gl_FragColor = (Idiff + Iamb + Ispec) * texColor;
            }
            """

    fragment_shader_bad = """
                // Внешние переменные, передаваемые из вершинного шейдера или установленные извне
                varying vec3 n; // Нормаль к поверхности в пространстве вида
                varying vec3 v; // Вектор от вершины к наблюдателю
                varying vec4 vertexColor; // Цвет вершины, передаваемый из вершинного шейдера

                uniform sampler2D tex; // Текстура, с которой будет взят цвет

                void main() {
                    // Вычисление вектора от поверхности к источнику света и к наблюдателю
                    vec3 L = normalize(gl_LightSource[0].position.xyz - v);
                    vec3 E = normalize(-v);

                    // Отраженный вектор относительно нормали
                    vec3 R = normalize(-reflect(L, n));

                    // Амбиентная составляющая освещения
                    vec4 Iamb = gl_FrontLightProduct[0].ambient;

                    // Диффузное освещение (Ламберта)
                    vec4 Idiff = gl_FrontLightProduct[0].diffuse * max(dot(n, L), 0.0);
                    Idiff = clamp(Idiff, 0.0, 1.0);

                    // Спекулярное освещение (Phong)
                    vec4 Ispec = gl_LightSource[0].specular * pow(max(dot(R, E), 0.0), gl_FrontMaterial.shininess);
                    Ispec = clamp(Ispec, 0.0, 1.0);

                    // Получение цвета текстуры по координатам текстуры
                    vec4 texColor = texture2D(tex, gl_TexCoord[0].st);

                    // Итоговый цвет фрагмента: комбинация освещения и текстуры
                    gl_FragColor = (Idiff + Iamb + Ispec) * texColor;
                }
            """

    vertex = create_shader(GL_VERTEX_SHADER, vertex_shader)
    fragment = create_shader(GL_FRAGMENT_SHADER, fragment_shader)
    # fragment = create_shader(GL_FRAGMENT_SHADER, fragment_shader_bad) # очень тёмные тени

    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    generate_texture()

    program = glCreateProgram()
    glAttachShader(program, vertex)
    glAttachShader(program, fragment)
    glLinkProgram(program)

    # используем массивы вершин, нормалей и цветов
    glEnableClientState(GL_VERTEX_ARRAY)
    glEnableClientState(GL_NORMAL_ARRAY)
    glEnableClientState(GL_COLOR_ARRAY)

    if texture_mode > 0:
        glEnableClientState(GL_TEXTURE_COORD_ARRAY) # используем текстуру

    renderPrism(0, 0, 0, radius, height, sides)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    # Устанавливает созданную шейдерную программу как текущую, чтобы все последующие вызовы отрисовки использовали эту программу.
    glUseProgram(program)

    while not glfw.window_should_close(window):
        display(window)

    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == '__main__':
    main()
