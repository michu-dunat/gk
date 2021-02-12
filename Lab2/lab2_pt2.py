import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import colorsys


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
    glClearColor(1.0, 1.0, 1.0, 1.0)
    update_viewport(None, 600, 600)


def shutdown():
    pass


def draw_mandelbrot_set(max_iteration):
    for px in range(-300, 301):
        for py in range(-300, 301):
            x0 = px / 150.0
            y0 = py / 150.0
            x = 0.0
            y = 0.0
            iteration = 0
            while x*x + y*y <= 2*2 and iteration < max_iteration:
                x_temp = x*x - y*y + x0
                y = 2*x*y + y0
                x = x_temp
                iteration = iteration + 1

            hue = int(255 * iteration / max_iteration)
            value = 255 if iteration < max_iteration else 0
            color = colorsys.hsv_to_rgb(hue / 255.0, 1.0, value / 255.0)
            glColor3f(color[0], color[1], color[2])
            glBegin(GL_POINTS)
            glVertex(px / 3, py / 3)
            glEnd()


def render(time):
    glClear(GL_COLOR_BUFFER_BIT)

    draw_mandelbrot_set(250)

    glFlush()


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(600, 600, __file__, None, None)
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