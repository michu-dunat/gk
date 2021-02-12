#!/usr/bin/env python3
import sys
from glfw.GLFW import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


viewer = [0.0, 0.0, 10.0]

theta, phi = 0.0, 0.0
pix2angle = 1.0

left_mouse_button_pressed, right_mouse_button_pressed = 0, 0
mouse_x_pos_old, mouse_y_pos_old = 0, 0
delta_x, delta_y = 0, 0

mat_ambient = [1.0, 1.0, 1.0, 1.0]
mat_diffuse = [1.0, 1.0, 1.0, 1.0]
mat_specular = [1.0, 1.0, 1.0, 1.0]
mat_shininess = 20.0

light_ambient = [0.1, 0.1, 0.0, 1.0]
light_diffuse = [0.8, 0.8, 0.0, 1.0]
light_specular = [1.0, 1.0, 1.0, 1.0]
light_position = [0.0, 0.0, 10.0, 1.0]

att_constant = 1.0
att_linear = 0.05
att_quadratic = 0.001

light1_ambient = [0.0, 0.0, 0.0, 1.0]
light1_diffuse = [0.0, 0.0, 1.0, 1.0]
light1_specular = [1.0, 1.0, 1.0, 1.0]
light1_position = [5.0, 5.0, -5.0, 1.0]

attribute_index = 0

r = 5.5

node_array, normal_vectors_array = None, None
N = 20

is_space_clicked = False


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialf(GL_FRONT, GL_SHININESS, mat_shininess)

    glLightfv(GL_LIGHT0, GL_AMBIENT, light_ambient)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, light_diffuse)
    glLightfv(GL_LIGHT0, GL_SPECULAR, light_specular)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)

    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)

    glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, att_constant)
    glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, att_linear)
    glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, att_quadratic)

    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_LIGHT1)

    fill_node_array()


def visualize_and_move_lights():
    global theta, phi, r
    global light_position, light1_position

    bounded_theta_to_rad = np.radians(theta % 360)
    bounded_phi_to_rad = np.radians(phi % 360)

    x = r * np.cos(bounded_theta_to_rad) * np.cos(bounded_phi_to_rad)
    y = r * np.sin(bounded_phi_to_rad)
    z = r * np.sin(bounded_theta_to_rad) * np.cos(bounded_phi_to_rad)

    light_position = [-x, y, z, 1.0]
    light1_position = [x, -y, -z, 1.0]

    glTranslate(-x, y, z)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glTranslate(x, -y, -z)

    glTranslate(x, -y, -z)
    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    gluSphere(quadric, 0.5, 6, 5)
    gluDeleteQuadric(quadric)
    glLightfv(GL_LIGHT1, GL_POSITION, light1_position)
    glTranslate(-x, y, z)


def fill_node_array():
    global node_array, normal_vectors_array, N

    node_array = np.zeros((N, N, 3))
    normal_vectors_array = np.zeros((N, N, 3))

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
                                   + 160 * u_array[i] ** 2) - 4.25
            # z
            node_array[i][j][2] = ((-90 * u_array[i] ** 5
                                    + 225 * u_array[i] ** 4
                                    - 270 * u_array[i] ** 3
                                    + 180 * u_array[i] ** 2
                                    - 45 * u_array[i])
                                   * np.sin(np.pi * v_array[j]))

            x_u = (-450 * u_array[i] ** 4
                   + 900 * u_array[i] ** 3
                   - 810 * u_array[i] ** 2
                   + 360 * u_array[i] - 45) * np.cos(np.pi * v_array[j])
            x_v = np.pi * (90 * u_array[i] ** 5
                           - 225 * u_array[i] ** 4
                           + 270 * u_array[i] ** 3
                           - 180 * u_array[i] ** 2
                           + 45 * u_array[i]) * np.sin(np.pi * v_array[j])
            y_u = (640 * u_array[i] ** 3
                   - 960 * u_array[i] ** 2
                   + 320 * u_array[i])
            z_u = (-450 * u_array[i] ** 4
                   + 900 * u_array[i] ** 3
                   - 810 * u_array[i] ** 2
                   + 360 * u_array[i] - 45) * np.sin(np.pi * v_array[j])
            z_v = -np.pi * (90 * u_array[i] ** 5
                            - 225 * u_array[i] ** 4
                            + 270 * u_array[i] ** 3
                            - 180 * u_array[i] ** 2
                            + 45 * u_array[i]) * np.cos(np.pi * v_array[j])

            if i == 0 or i == N:
                normal_vectors_array[i][j] = [0, -1, 0]
                continue
            elif i == N / 2:
                normal_vectors_array[i][j] = [0, 1, 0]

            normal_vectors_array[i][j] = [y_u * z_v - z_u * 0,
                                          z_u * x_v - x_u * z_v,
                                          x_u * 0 - y_u * x_v]
            normal_vector_length = np.sqrt(normal_vectors_array[i][j][0] ** 2
                                           + normal_vectors_array[i][j][1] ** 2
                                           + normal_vectors_array[i][j][2] ** 2)
            if i < N / 2:
                normal_vectors_array[i][j] = np.divide(normal_vectors_array[i][j],
                                                       normal_vector_length)
            else:
                normal_vectors_array[i][j] = np.divide(normal_vectors_array[i][j],
                                                       -normal_vector_length)


def draw_egg_model_with_triangles():
    global is_space_clicked

    for i in range(0, N - 1):
        for j in range(0, N - 1):
            glBegin(GL_TRIANGLES)
            glNormal3fv(normal_vectors_array[i][j])
            glVertex3f(node_array[i][j][0],
                          node_array[i][j][1],
                          node_array[i][j][2])
            glNormal3fv(normal_vectors_array[i + 1][j])
            glVertex3f(node_array[i + 1][j][0],
                          node_array[i + 1][j][1],
                          node_array[i + 1][j][2])
            glNormal3fv(normal_vectors_array[i][j + 1])
            glVertex3f(node_array[i][j + 1][0],
                          node_array[i][j + 1][1],
                          node_array[i][j + 1][2])
            glEnd()

            glBegin(GL_TRIANGLES)
            glNormal3fv(normal_vectors_array[i + 1][j])
            glVertex3f(node_array[i + 1][j][0],
                          node_array[i + 1][j][1],
                          node_array[i + 1][j][2])
            glNormal3fv(normal_vectors_array[i][j + 1])
            glVertex3f(node_array[i][j + 1][0],
                          node_array[i][j + 1][1],
                          node_array[i][j + 1][2])
            glNormal3fv(normal_vectors_array[i + 1][j + 1])
            glVertex3f(node_array[i + 1][j + 1][0],
                          node_array[i + 1][j + 1][1],
                          node_array[i + 1][j + 1][2])
            glEnd()

            # draw normal vectors
            if is_space_clicked:
                glBegin(GL_LINES)
                glVertex(node_array[i][j])
                glVertex(node_array[i][j] + normal_vectors_array[i][j])
                glEnd()


def shutdown():
    pass


def render(time):
    global theta, phi

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    gluLookAt(viewer[0], viewer[1], viewer[2],
              0.0, 0.0, 0.0, 0.0, 1.0, 0.0)

    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle

    draw_egg_model_with_triangles()

    visualize_and_move_lights()

    glFlush()


def update_viewport(window, width, height):
    global pix2angle
    pix2angle = 360.0 / width

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(70, 1.0, 0.1, 300.0)

    if width <= height:
        glViewport(0, int((height - width) / 2), width, width)
    else:
        glViewport(int((width - height) / 2), 0, height, height)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


def change_value(is_to_be_increased):
    global attribute_index
    global light1_ambient, light1_diffuse, light1_specular

    if attribute_index == 0 or attribute_index == 1 or attribute_index == 2:
        if is_to_be_increased:
            light1_ambient[attribute_index % 3] += 0.1 if light1_ambient[attribute_index % 3] <= 0.9 else 0.0
            print(f"light1_ambient[{attribute_index % 3}] = {round(light1_ambient[attribute_index % 3], 2)}")
        else:
            light1_ambient[attribute_index % 3] -= 0.1 if light1_ambient[attribute_index % 3] >= 0.1 else 0.0
            print(f"light1_ambient[{attribute_index % 3}] = {round(light1_ambient[attribute_index % 3], 2)}")
        glLightfv(GL_LIGHT1, GL_AMBIENT, light1_ambient)
    elif attribute_index == 3 or attribute_index == 4 or attribute_index == 5:
        if is_to_be_increased:
            light1_diffuse[attribute_index % 3] += 0.1 if light1_diffuse[attribute_index % 3] <= 0.9 else 0.0
            print(f"light1_diffuse[{attribute_index % 3}] = {round(light1_diffuse[attribute_index % 3], 2)}")
        else:
            light1_diffuse[attribute_index % 3] -= 0.1 if light1_diffuse[attribute_index % 3] >= 0.1 else 0.0
            print(f"light1_diffuse[{attribute_index % 3}] = {round(light1_diffuse[attribute_index % 3], 2)}")
        glLightfv(GL_LIGHT1, GL_DIFFUSE, light1_diffuse)
    elif attribute_index == 6 or attribute_index == 7 or attribute_index == 8:
        if is_to_be_increased:
            light1_specular[attribute_index % 3] += 0.1 if light1_specular[attribute_index % 3] <= 0.9 else 0.0
            print(f"light1_specular[{attribute_index % 3}] = {round(light1_specular[attribute_index % 3], 2)}")
        else:
            light1_specular[attribute_index % 3] -= 0.1 if light1_specular[attribute_index % 3] >= 0.1 else 0.0
            print(f"light1_specular[{attribute_index % 3}] = {round(light1_specular[attribute_index % 3], 2)}")
        glLightfv(GL_LIGHT1, GL_SPECULAR, light1_specular)


def keyboard_key_callback(window, key, scancode, action, mods):
    global attribute_index
    global is_space_clicked

    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)
    if key == GLFW_KEY_1 and action == GLFW_PRESS:
        attribute_index = 0
    if key == GLFW_KEY_2 and action == GLFW_PRESS:
        attribute_index = 1
    if key == GLFW_KEY_3 and action == GLFW_PRESS:
        attribute_index = 2
    if key == GLFW_KEY_4 and action == GLFW_PRESS:
        attribute_index = 3
    if key == GLFW_KEY_5 and action == GLFW_PRESS:
        attribute_index = 4
    if key == GLFW_KEY_6 and action == GLFW_PRESS:
        attribute_index = 5
    if key == GLFW_KEY_7 and action == GLFW_PRESS:
        attribute_index = 6
    if key == GLFW_KEY_8 and action == GLFW_PRESS:
        attribute_index = 7
    if key == GLFW_KEY_9 and action == GLFW_PRESS:
        attribute_index = 8
    if key == GLFW_KEY_W and action == GLFW_PRESS:
        change_value(True)
    if key == GLFW_KEY_S and action == GLFW_PRESS:
        change_value(False)
    if key == GLFW_KEY_SPACE and action == GLFW_PRESS:
        is_space_clicked = not is_space_clicked


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0


def main():
    if not glfwInit():
        sys.exit(-1)

    window = glfwCreateWindow(400, 400, __file__, None, None)
    if not window:
        glfwTerminate()
        sys.exit(-1)

    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, update_viewport)
    glfwSetKeyCallback(window, keyboard_key_callback)
    glfwSetCursorPosCallback(window, mouse_motion_callback)
    glfwSetMouseButtonCallback(window, mouse_button_callback)
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
