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

r = 1.0
tab_pressed = 0


def startup():
    update_viewport(None, 400, 400)
    glClearColor(0.0, 0.0, 0.0, 1.0)
    glEnable(GL_DEPTH_TEST)


def call_gluLookAt(x, y, z):
    gluLookAt(x, y, z, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0)


def calculate_theta_phi_on_left_mouse_button_pressed(theta, phi):
    if left_mouse_button_pressed:
        theta += delta_x * pix2angle
        phi += delta_y * pix2angle
    return theta, phi


def calculate_x_y_z_of_eye(theta, phi):
    global r

    bounded_theta_to_rad = abs(np.radians(theta % 360))
    bounded_phi_to_rad = abs(np.radians(phi % 360))

    x_eye = r * np.cos(bounded_theta_to_rad) * np.cos(bounded_phi_to_rad)
    y_eye = r * np.sin(bounded_phi_to_rad)
    z_eye = r * np.sin(bounded_theta_to_rad) * np.cos(bounded_phi_to_rad)

    return x_eye, y_eye, z_eye


def rotate_object():
    global theta, phi

    call_gluLookAt(viewer[0], viewer[1], viewer[2])

    theta, phi = calculate_theta_phi_on_left_mouse_button_pressed(theta, phi)

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)


def rotate_and_scale_object():
    global theta, phi, r

    call_gluLookAt(viewer[0], viewer[1], viewer[2])

    theta, phi = calculate_theta_phi_on_left_mouse_button_pressed(theta, phi)
    if right_mouse_button_pressed:
        r += 0.005 * delta_y

    glRotatef(theta, 0.0, 1.0, 0.0)
    glRotatef(phi, 1.0, 0.0, 0.0)
    glScalef(r, r, r)


def move_camera():
    global theta, phi, r

    call_gluLookAt(viewer[0], viewer[1], viewer[2])

    theta, phi = calculate_theta_phi_on_left_mouse_button_pressed(theta, phi)
    if right_mouse_button_pressed:
        r += 0.05 * delta_y

    x, y, z = calculate_x_y_z_of_eye(theta, phi)

    call_gluLookAt(x, y, z)


def move_camera_with_bounds_and_proper_transitions():
    global theta, phi, r

    call_gluLookAt(viewer[0], viewer[1], viewer[2])

    theta, phi = calculate_theta_phi_on_left_mouse_button_pressed(theta, phi)
    if right_mouse_button_pressed:
        r += 0.05 * delta_y
        if r > 50:
            r = 49.99
        if r <= 0:
            r = 0.01

    x, y, z = calculate_x_y_z_of_eye(theta, phi)

    if phi % 360 < 90 and phi % 360 > 270:
        call_gluLookAt(x, y, z)
    else:
        gluLookAt(x, y, z, 0.0, 0.0, 0.0, 0.0, -1.0, 0.0)


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


def example_object():
    glColor3f(1.0, 1.0, 1.0)

    quadric = gluNewQuadric()
    gluQuadricDrawStyle(quadric, GLU_LINE)
    glRotatef(90, 1.0, 0.0, 0.0)
    glRotatef(-90, 0.0, 1.0, 0.0)

    gluSphere(quadric, 1.5, 10, 10)

    glTranslatef(0.0, 0.0, 1.1)
    gluCylinder(quadric, 1.0, 1.5, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, -1.1)

    glTranslatef(0.0, 0.0, -2.6)
    gluCylinder(quadric, 0.0, 1.0, 1.5, 10, 5)
    glTranslatef(0.0, 0.0, 2.6)

    glRotatef(90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(-90, 1.0, 0.0, 1.0)

    glRotatef(-90, 1.0, 0.0, 1.0)
    glTranslatef(0.0, 0.0, 1.5)
    gluCylinder(quadric, 0.1, 0.0, 1.0, 5, 5)
    glTranslatef(0.0, 0.0, -1.5)
    glRotatef(90, 1.0, 0.0, 1.0)

    glRotatef(90, 0.0, 1.0, 0.0)
    glRotatef(-90, 1.0, 0.0, 0.0)
    gluDeleteQuadric(quadric)


def render(time):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # 3.0
    #rotate_object()

    # 3.5
    #rotate_and_scale_object()

    # 4.0
    #move_camera()

    # 4.5
    if tab_pressed:
        rotate_and_scale_object()
    else:
        move_camera_with_bounds_and_proper_transitions()

    axes()
    example_object()

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


def keyboard_key_callback(window, key, scancode, action, mods):
    if key == GLFW_KEY_ESCAPE and action == GLFW_PRESS:
        glfwSetWindowShouldClose(window, GLFW_TRUE)

    global tab_pressed
    if key == GLFW_KEY_TAB and action == GLFW_PRESS:
        tab_pressed = not tab_pressed


def mouse_motion_callback(window, x_pos, y_pos):
    global delta_x, delta_y
    global mouse_x_pos_old, mouse_y_pos_old

    delta_x = x_pos - mouse_x_pos_old
    mouse_x_pos_old = x_pos

    delta_y = y_pos - mouse_y_pos_old
    mouse_y_pos_old = y_pos


def mouse_button_callback(window, button, action, mods):
    global left_mouse_button_pressed, right_mouse_button_pressed

    if button == GLFW_MOUSE_BUTTON_LEFT and action == GLFW_PRESS:
        left_mouse_button_pressed = 1
    else:
        left_mouse_button_pressed = 0

    if button == GLFW_MOUSE_BUTTON_RIGHT and action == GLFW_PRESS:
        right_mouse_button_pressed = 1
    else:
        right_mouse_button_pressed = 0


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
