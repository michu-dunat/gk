import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import random


def update_viewport(window, width, height):
    if height == 0:
        height = 1
    if width == 0:
        width = 1
    aspectRatio = width / height

    glMatrixMode(GL_PROJECTION)
    glViewport(0, 0, width, height)
    glLoadIdentity()

    if width <= height:
        glOrtho(-100.0, 100.0, -100.0 / aspectRatio, 100.0 / aspectRatio,
                   1.0, -1.0)
    else:
        glOrtho(-100.0 * aspectRatio, 100.0 * aspectRatio, -100.0, 100.0,
                   1.0, -1.0)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def startup():
    glClearColor(240 / 255.0, 255 / 255.0, 255 / 255.0, 1.0)
    update_viewport(None, 400, 400)


def shutdown():
    pass


def draw_triangle():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    glVertex2f(-50.0, 0.0)
    glColor3f(0.0, 1.0, 0.0)
    glVertex2f(0.0, 50.0)
    glColor3f(0.0, 0.0, 1.0)
    glVertex2f(50.0, 0.0)
    glEnd()


def draw_rectangle(x, y, a, b):
    if x < -100:
        x = -100
    if y > 100:
        y = 100
    if x + b > 100:
        x = 100 - b
    if y - a < -100:
        y = -100 + a

    glColor3f(139 / 255.0, 69 / 255.0, 19 / 255.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, y-a)
    glVertex2f(x+b, y-a)
    glEnd()

    glColor3f(139 / 255.0, 69 / 255.0, 19 / 255.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x+b, y)
    glVertex2f(x+b, y-a)
    glEnd()


def draw_rectangle_white(x, y, a, b):
    if x < -100:
        x = -100
    if y > 100:
        y = 100
    if x + b > 100:
        x = 100 - b
    if y - a < -100:
        y = -100 + a

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, y-a)
    glVertex2f(x+b, y-a)
    glEnd()

    glColor3f(1.0, 1.0, 1.0)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x+b, y)
    glVertex2f(x+b, y-a)
    glEnd()


RED = random.random()
GREEN = random.random()
BLUE = random.random()


def draw_rectangle_ver2(x, y, a, b, d=0):
    if x < -100:
        x = -100
    if y > 100:
        y = 100
    if x + b > 100:
        x = 100 - b
    if y - a < -100:
        y = -100 + a

    a = a * d
    b = b * d

    glColor3f(RED, GREEN, BLUE)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x, y-a)
    glVertex2f(x+b, y-a)
    glEnd()

    glColor3f(RED, GREEN, BLUE)
    glBegin(GL_TRIANGLES)
    glVertex2f(x, y)
    glVertex2f(x+b, y)
    glVertex2f(x+b, y-a)
    glEnd()


def draw_sierpinski(x, y, a, b, level):
    if level > 0:
        new_x = x + (b / 3.0)
        new_y = y - (a / 3.0)
        new_a = a / 3.0
        new_b = b / 3.0
        draw_rectangle_white(new_x, new_y, new_a, new_b)
        if level > 1:
            for i in range(0, 3):
                for j in range(0, 3):
                    if i == 1 and j == 1:
                        continue 
                    draw_sierpinski(x + (new_b * i), y - (new_a * j),
                                    new_a, new_b, level - 1)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    # 3.0
    #draw_triangle()

    # 3.5
    #draw_rectangle(0, 0, 50, 100)

    # 4.0
    #draw_rectangle_ver2(0, 0, 50, 100, 0.75)

    # 4.5
    draw_rectangle(-100, 100, 100, 150)
    draw_sierpinski(-100, 100, 100, 150, 5)

    glFlush()


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
