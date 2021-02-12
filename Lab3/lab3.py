import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np
import random


def spin(angle):
    glRotatef(angle, 1.0, 0.0, 0.0)
    glRotatef(angle, 0.0, 1.0, 0.0)
    glRotatef(angle, 0.0, 0.0, 1.0)


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    global N
    global node_colors_array
    global node_array

    N = 45
    node_array = create_fill_return_node_array(N)

    node_colors_array = np.zeros((N, N, 8))
    for i in range(0, N):
        for j in range(0, N - 1):
            for k in range(0, 8):
                node_colors_array[i][j][k] = random.random()
    for i in range(0, N):
            node_colors_array[i][N - 1][0] = node_colors_array[N - 1 - i][0][0]
            node_colors_array[i][N - 1][1] = node_colors_array[N - 1 - i][0][1]
            node_colors_array[i][N - 1][2] = node_colors_array[N - 1 - i][0][2]


def create_fill_return_node_array(N):
    node_array = np.zeros((N, N, 3))

    u_array = [u / (N - 1) for u in range(0, N)]
    v_array = [v / (N - 1) for v in range(0, N)]

    for i in range(0, N):
        for j in range(0, N):
            # x
            node_array[i][j][0] = ((-90 * u_array[i] ** 5
                                   + 225 * u_array[i] ** 4
                                   - 270 * u_array[i] ** 3
                                   + 180 * u_array[i] ** 2
                                   - 45 * u_array[i])
                                   * np.cos(np.pi * v_array[j]))
            # y
            node_array[i][j][1] = (160 * u_array[i] ** 4
                                   - 320 * u_array[i] ** 3
                                   + 160 * u_array[i] ** 2) - 0.05
            # z
            node_array[i][j][2] = ((-90 * u_array[i] ** 5
                                    + 225 * u_array[i] ** 4
                                    - 270 * u_array[i] ** 3
                                    + 180 * u_array[i] ** 2
                                    - 45 * u_array[i])
                                   * np.sin(np.pi * v_array[j]))

    return node_array


def draw_egg_model_with_points():
    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_POINTS)
    for i in range(0, N):
        for j in range(0, N):
            glVertex3f(node_array[i][j][0],
                          node_array[i][j][1],
                          node_array[i][j][2])
    glEnd()


def draw_egg_model_with_lines():
    glColor3f(1.0, 1.0, 1.0)
    for i in range(0, N - 1):
        for j in range(0, N - 1):
            glBegin(GL_LINES)
            glVertex3f(node_array[i][j][0],
                          node_array[i][j][1],
                          node_array[i][j][2])
            glVertex3f(node_array[i + 1][j][0],
                          node_array[i + 1][j][1],
                          node_array[i + 1][j][2])
            glEnd()

            glBegin(GL_LINES)
            glVertex3f(node_array[i][j][0],
                          node_array[i][j][1],
                          node_array[i][j][2])
            glVertex3f(node_array[i][j + 1][0],
                          node_array[i][j + 1][1],
                          node_array[i][j + 1][2])
            glEnd()


def draw_egg_model_with_triangles():
    for i in range(0, N - 1):
        for j in range(0, N - 1):
            glBegin(GL_TRIANGLES)
            glColor3f(node_colors_array[i][j][0],
                         node_colors_array[i][j][1],
                         node_colors_array[i][j][2])
            glVertex3f(node_array[i][j][0],
                          node_array[i][j][1],
                          node_array[i][j][2])
            glColor3f(node_colors_array[i][j][1],
                         node_colors_array[i][j][2],
                         node_colors_array[i][j][3])
            glVertex3f(node_array[i + 1][j][0],
                          node_array[i + 1][j][1],
                          node_array[i + 1][j][2])
            glColor3f(node_colors_array[i][j][2],
                         node_colors_array[i][j][3],
                         node_colors_array[i][j][4])
            glVertex3f(node_array[i][j + 1][0],
                          node_array[i][j + 1][1],
                          node_array[i][j + 1][2])
            glEnd()

            glBegin(GL_TRIANGLES)
            glColor3f(node_colors_array[i + 1][j][3],
                         node_colors_array[i + 1][j][4],
                         node_colors_array[i + 1][j][5])
            glVertex3f(node_array[i + 1][j][0],
                          node_array[i + 1][j][1],
                          node_array[i + 1][j][2])
            glColor3f(node_colors_array[i][j][4],
                         node_colors_array[i][j][5],
                         node_colors_array[i][j][6])
            glVertex3f(node_array[i][j + 1][0],
                          node_array[i][j + 1][1],
                          node_array[i][j + 1][2])
            glColor3f(node_colors_array[i][j][5],
                         node_colors_array[i][j][6],
                         node_colors_array[i][j][7])
            glVertex3f(node_array[i + 1][j + 1][0],
                          node_array[i + 1][j + 1][1],
                          node_array[i + 1][j + 1][2])
            glEnd()


def draw_egg_model_with_triangle_strip():
    glBegin(GL_TRIANGLE_STRIP)
    for i in range(N - 1):
        for j in range(N - 1):
            if (j != N - 2):
                glColor3f(node_colors_array[i][j][0],
                             node_colors_array[i][j][1],
                             node_colors_array[i][j][2])
                glVertex3f(node_array[i][j][0],
                              node_array[i][j][1],
                              node_array[i][j][2])
                glColor3f(node_colors_array[i][j + 1][0],
                             node_colors_array[i][j + 1][1],
                             node_colors_array[i][j + 1][2])
                glVertex3f(node_array[i][j + 1][0],
                              node_array[i][j + 1][1],
                              node_array[i][j + 1][2])
                glColor3f(node_colors_array[i + 1][j][0],
                             node_colors_array[i + 1][j][1],
                             node_colors_array[i + 1][j][2])
                glVertex3f(node_array[i + 1][j][0],
                              node_array[i + 1][j][1],
                              node_array[i + 1][j][2])
                glColor3f(node_colors_array[i + 1][j + 1][0],
                             node_colors_array[i + 1][j + 1][1],
                             node_colors_array[i + 1][j + 1][2])
                glVertex3f(node_array[i + 1][j + 1][0],
                              node_array[i + 1][j + 1][1],
                              node_array[i + 1][j + 1][2])
            else:
                glColor3f(node_colors_array[i][j][0],
                             node_colors_array[i][j][1],
                             node_colors_array[i][j][2])
                glVertex3f(node_array[i][j][0],
                              node_array[i][j][1],
                              node_array[i][j][2])
                glColor3f(node_colors_array[i][j + 1][0],
                             node_colors_array[i][j + 1][1],
                             node_colors_array[i][j + 1][2])
                glVertex3f(node_array[i][j + 1][0],
                              node_array[i][j + 1][1],
                              node_array[i][j + 1][2])
                glColor3f(node_colors_array[i + 1][j][0],
                             node_colors_array[i + 1][j][1],
                             node_colors_array[i + 1][j][0])
                glVertex3f(node_array[i + 1][j][0],
                              node_array[i + 1][j][1],
                              node_array[i + 1][j][2])
                glColor3f(node_colors_array[i + 1][j + 1][0],
                             node_colors_array[i + 1][j + 1][1],
                             node_colors_array[i + 1][j + 1][0])
                glVertex3f(node_array[i + 1][j + 1][0],
                              node_array[i + 1][j + 1][1],
                              node_array[i + 1][j + 1][2])
    glEnd()


def shutdown():
    pass


def axes():
    glBegin(GL_LINES)

    glColor3f(1.0, 0.0, 0.0)
    glVertex3f(-5.0, 0.0, 0.0)
    glVertex3f(5.0, 0.0, 0.0)

    glColor3f(0.0, 1.0, 0.0)
    glVertex3f(0.0, -5.0, 0.0)
    glVertex3f(0.0, 5.0, 0.0)

    glColor3f(0.0, 0.0, 1.0)
    glVertex3f(0.0, 0.0, -5.0)
    glVertex3f(0.0, 0.0, 5.0)

    glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    axes()

    # 3.0
    #draw_egg_model_with_points()

    # 3.5
    #spin(time * 180 / np.pi)
    #draw_egg_model_with_lines()

    # 4.0
    #draw_egg_model_with_triangles()

    # 4.5
    draw_egg_model_with_triangle_strip()

    glFlush()


def update_viewport(window, width, height):
    if width == 0:
        width = 1
    if height == 0:
        height = 1
    aspect_ratio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-10, 10, -10 / aspect_ratio, 10 / aspect_ratio, 10, -10)
    else:
        glOrtho(-10 * aspect_ratio, 10 * aspect_ratio, -10, 10, 10, -10)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSwapInterval(1)

    startup()
    while not glfwWindowShouldClose(window):
        render(glfwGetTime())
        glfwSwapBuffers(window)
        glfwPollEvents()
    shutdown()

    glfwTerminate()


if __name__ == '__main__':
    main()
