from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 500, 500

balls = []

speed = 2
ball_size = 6
functionality_flag = True
blinking = False

class point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0


class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        direction = random.choice([(-1, 1), (-1, -1), (1, 1), (1, -1)])
        self.dx = direction[0] * speed
        self.dy = direction[1] * speed
        self.color = (random.random(), random.random(), random.random())  # Random color
        self.size = ball_size
        self.temp_color = None


def crossProduct(a, b):
    result = point()
    result.x = a.y * b.z - a.z * b.y
    result.y = a.z * b.x - a.x * b.z
    result.z = a.x * b.y - a.y * b.x
    return result


def convert_coordinate(x, y):
    global W_Width, W_Height
    a = x - (W_Width / 2)
    b = (W_Height / 2) - y
    return a, b


def draw_points(ball):
    glPointSize(ball.size)
    glBegin(GL_POINTS)
    glColor3f(ball.color[0], ball.color[1], ball.color[2])
    glVertex2f(ball.x, ball.y)
    glEnd()


def drawShapes():
    pass


def keyboardListener(key, x, y):
    global ball_size
    # if key == b'w':
    #     ball_size += 1
    #     print("Size Increased")
    # if key == b's':
    #     ball_size -= 1
    #     print("Size Decreased")
    if key == b' ':
        global functionality_flag
        functionality_flag = not functionality_flag #pause and unpause
        print("Functionality Toggled: ", functionality_flag)
    glutPostRedisplay()


def specialKeyListener(key, x, y):
    global functionality_flag
    if functionality_flag==False:
        return
    global speed
    if key == GLUT_KEY_UP:
        speed += 0.1
        for ball in balls:
            ball.dx = (ball.dx / abs(ball.dx)) * speed
            ball.dy = (ball.dy / abs(ball.dy)) * speed
        print("Speed Increased")

    if key == GLUT_KEY_DOWN:
        speed -= 0.1
        if speed > 0:
            for ball in balls:
                ball.dx = (ball.dx / abs(ball.dx)) * speed
                ball.dy = (ball.dy / abs(ball.dy)) * speed
            print("Speed Decreased")
        else:
            speed = 5


def toggle_blink(value):
    global blinking
    if blinking==False:
        for ball in balls:
            if ball.temp_color:
                ball.color = ball.temp_color # returning to original color
        return

    if value == 0:
        for ball in balls:
            ball.temp_color = ball.color
            ball.color = (0, 0, 0)  # Set color to black
        glutTimerFunc(1000, toggle_blink, 1)  # Restore colors after 1000ms (1 second)
    if value == 1:
        for ball in balls:
            ball.color = ball.temp_color  # returning to original color
        if blinking:  # Check if blinking is still True
            glutTimerFunc(1000, toggle_blink, 0)  # Toggle back to blinking after 1000ms (1 second)

    glutPostRedisplay()


def mouseListener(button, state, x, y):
    global functionality_flag
    global speed
    global blinking

    if functionality_flag==False:
        return

    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN:
        print(x, y)
        c_X, c_y = convert_coordinate(x, y)
        new_ball = Ball(c_X, c_y)
        direction = random.choice([(-1, 1), (-1, -1), (1, 1), (1, -1)])
        new_ball.dx = direction[0] * speed
        new_ball.dy = direction[1] * speed
        balls.append(new_ball)
    glutPostRedisplay()

    if button == GLUT_LEFT_BUTTON: #hold down left mouse button to start blinking
        if state == GLUT_DOWN:
            blinking = True
            glutTimerFunc(0, toggle_blink, 0)  # Start blinking immediately
        elif state == GLUT_UP: #stop blinking by leaving the button
            blinking = False
            for ball in balls:
                if ball.temp_color:
                    ball.color = ball.temp_color #return to original color
        print("Blinking: ", blinking)
    glutPostRedisplay()


def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    for ball in balls:
        draw_points(ball)
    drawShapes()
    glutSwapBuffers()


def animate():
    glutPostRedisplay()
    global functionality_flag
    if functionality_flag==False:
        return
    for ball in balls:
        ball.x += ball.dx
        ball.y += ball.dy
        if ball.x <= -W_Width / 2 or ball.x >= W_Width / 2: #to make sure the ball bouncess
            ball.dx = -ball.dx
        if ball.y <= -W_Height / 2 or ball.y >= W_Height / 2: #to make sure the ball bouncess
            ball.dy = -ball.dy


def init():
    glClearColor(0, 0, 0, 0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)


glutInit()
glutInitWindowSize(W_Width, W_Height)
glutInitWindowPosition(0, 0)
glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)

wind = glutCreateWindow(b"Bouncing balls")
init()

glutDisplayFunc(display)
glutIdleFunc(animate)
glutKeyboardFunc(keyboardListener)
glutSpecialFunc(specialKeyListener)
glutMouseFunc(mouseListener)

glutMainLoop()
