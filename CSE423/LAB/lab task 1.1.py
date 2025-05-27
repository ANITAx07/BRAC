from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random

W_Width, W_Height = 650, 650

rain_speed = 5
num_raindrops = 100
raindrops=[]
#here I am creating random raindrops that will have different lengths. Used width//2 and height//2 for x and y to make sure they are withing our defined axis
for i in range(num_raindrops):
    x = random.randint(-W_Width // 2, W_Width // 2) #random x points
    y = random.randint(50, W_Height // 2) #random y points
    size = random.randint(9, 15) # here using random function I am getting random value from 10.0<=x<15.0, this will be used to make raindrops of different sizes
    raindrops.append((x, y, size)) 
bend = 0 #to facilitate wind direction
r = 0.0
g = 0.0
b = 0.0
s = 0.0

# Color states and colors 
background_colors = [r, g, b, s]
current_color_index = 0

class point:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

def crossProduct(a, b): #did not have to use
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

def draw_points(x, y, s):
    glPointSize(s)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def drawShapes():
    scale = 0.8 # I wanted to make it so I can change the full size of the house by changing one value, so this scales the house
    glLineWidth(4)
    # House roof
    glBegin(GL_TRIANGLES)
    glColor3d(0.615, 0.376, 0.333)
    glVertex2f(5 * scale, 200 * scale)
    glVertex2f(-250 * scale, 5 * scale)
    glVertex2f(250 * scale, 5 * scale)
    glEnd()

    # House outline
    glColor3f(0.5, 0.4, 0.4)
    glBegin(GL_LINES)
    glVertex2f(-250 * scale, 5 * scale)
    glVertex2f(-250 * scale, -250 * scale)
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(-250 * scale, -250 * scale)
    glVertex2f(250 * scale, -250 * scale)
    glEnd()

    glBegin(GL_LINES)
    glVertex2f(250 * scale, -250 * scale)
    glVertex2f(250 * scale, 5 * scale)
    glEnd()

    # Door
    glColor3f(0.3, 0.2, 0.1)
    glBegin(GL_LINES)
    glVertex2f(-80 * scale, -250 * scale)
    glVertex2f(-80 * scale, -100 * scale)

    glVertex2f(-80 * scale, -100 * scale)
    glVertex2f(10 * scale, -100 * scale)

    glVertex2f(10 * scale, -100 * scale)
    glVertex2f(10 * scale, -250 * scale)

    glVertex2f(10 * scale, -250 * scale)
    glVertex2f(-80 * scale, -250 * scale)
    glEnd()

    # Door knob
    glColor3f(1.0, 1.0, 0.0)
    glPointSize(10)
    glBegin(GL_POINTS)
    glVertex2f(-20 * scale, -175 * scale)
    glEnd()

    # Window
    glColor3f(0.7, 0.7, 1.0)
    glBegin(GL_LINES)
    glVertex2f(100 * scale, -185 * scale)
    glVertex2f(100 * scale, -80 * scale)

    glVertex2f(100 * scale, -80 * scale)
    glVertex2f(220 * scale, -80 * scale)

    glVertex2f(220 * scale, -80 * scale)
    glVertex2f(220 * scale, -185 * scale)

    glVertex2f(220 * scale, -185 * scale)
    glVertex2f(100 * scale, -185 * scale)
    glEnd()
def draw_rain():
    glColor3f(0.0, 0.0, 1.0)
    glLineWidth(2)
    glBegin(GL_LINES)
    for x, y, size in raindrops:
        glVertex2f(x, y)
        glVertex2f(x + bend, y -size)  # endpoint of each line Adjust for  movement of the wind changing as for changing x the wind will go sideways 
    glEnd()

def keyboardListener(key, x, y):
    glutPostRedisplay()

def specialKeyListener(key, x, y):
    global rain_speed, bend
    if key == GLUT_KEY_UP:
        rain_speed += 1
        print(f"Rain speed increased to {rain_speed}")
    elif key == GLUT_KEY_DOWN:
        if rain_speed > 1:
            rain_speed -= 1
            print(f"Rain speed decreased to {rain_speed}")
    elif key == GLUT_KEY_RIGHT:
        bend += 1
        print(f"Wind towards SE")
    elif key == GLUT_KEY_LEFT:
        bend -= 1
        print(f"Wind towards SW")
    glutPostRedisplay()

def mouseListener(button, state, x, y):
    global background_colors
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN: #each click will time go forward
        background_colors[0] += 0.1
        background_colors[1] += 0.1
        background_colors[2] += 0.1
        if 0 <= background_colors[0] <= 1:
            print(f"Background color changed to {background_colors[current_color_index]}")
            glutSetWindow(wind)
            glClearColor(*tuple(background_colors))
    if button == GLUT_RIGHT_BUTTON and state == GLUT_DOWN: #each click will time go backwards
        background_colors[0] -= 0.1
        background_colors[1] -= 0.1
        background_colors[2] -= 0.1
        if 0 <= background_colors[0] < 1:
            print(f"Background color changed to {background_colors[current_color_index]}")
            glutSetWindow(wind)
            glClearColor(*tuple(background_colors))
        glutPostRedisplay()



def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 0, 200, 0, 0, 0, 0, 1, 0)
    
    draw_rain()
    drawShapes()

    glutSwapBuffers()

def animate():
    glutPostRedisplay()
    global raindrops
    for i in range(len(raindrops)):
        x, y, size = raindrops[i]
        x += bend
        y -= rain_speed
        if y < 50: #corner case to make sure the rain does not cross the house
            y = W_Height // 2 # resetting the y value to top
            x = random.randint(-W_Width // 2, W_Width // 2) #setting the x value in a random point in the x axis
        if y < -W_Height // 2: #corner case to make sure that the rain does not go out of bounds
            y = W_Height // 2# resetting the y value to top
            x = random.randint(-W_Width // 2, W_Width // 2)#setting the x value in a random point in the x axis
        if x > W_Width // 2: #corner case to make sure that the rain does not go out of bounds
            x = -W_Width // 2 #this is used so that the rain wraps around after bending too much
        elif x < -W_Width // 2: #corner case to make sure that the rain does not go out of bounds
            x = W_Width // 2 #this is used so that the rain wraps around after bending too much
        raindrops[i] = (x, y, size)

def init():
    global wind
    glutInit()
    glutInitWindowSize(W_Width, W_Height)
    glutInitWindowPosition(0, 0)
    glutInitDisplayMode(GLUT_DEPTH | GLUT_DOUBLE | GLUT_RGB)
    wind = glutCreateWindow(b"Heavy Rain")
    glClearColor(*tuple(background_colors))
    glutDisplayFunc(display)
    glutIdleFunc(animate)
    glutKeyboardFunc(keyboardListener)
    glutSpecialFunc(specialKeyListener)
    glutMouseFunc(mouseListener)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(104, 1, 1, 1000.0)

init()
glutMainLoop()
