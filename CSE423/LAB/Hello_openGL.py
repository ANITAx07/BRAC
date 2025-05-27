from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Screen dimensions
WIDTH, HEIGHT = 800, 600

# Game variables
catcher_pos = WIDTH // 2
diamond_pos = [random.randint(0, WIDTH - 20), HEIGHT]
diamond_speed = 150  # Starting speed
score = 0
game_state = 'playing'

# Colors
WHITE = (1.0, 1.0, 1.0)
RED = (1.0, 0.0, 0.0)
TEAL = (0.0, 1.0, 1.0)
AMBER = (1.0, 0.75, 0.0)
BACKGROUND = (0.0, 0.0, 0.0)

# Time variables for delta timing
last_time = time.time()
delta_time = 0

# Button dimensions
BUTTON_WIDTH, BUTTON_HEIGHT = 80, 80
BUTTON_PADDING = 20

def init():
    glClearColor(*BACKGROUND, 1.0)
    gluOrtho2D(0, WIDTH, 0, HEIGHT)

def draw_midpoint_line(x1, y1, x2, y2):
    glBegin(GL_POINTS)
    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)  # Ensure all values are integers
    dx = abs(x2 - x1)
    dy = abs(y2 - y1)
    sx = 1 if x1 < x2 else -1
    sy = 1 if y1 < y2 else -1
    err = dx - dy

    while True:
        glVertex2i(x1, y1)
        if x1 == x2 and y1 == y2:
            break
        e2 = err * 2
        if e2 > -dy:
            err -= dy
            x1 += sx
        if e2 < dx:
            err += dx
            y1 += sy
    glEnd()

def draw_catcher():
    x = catcher_pos
    y = 50
    color = WHITE if game_state != 'game over' else RED
    glColor3f(*color)
    draw_midpoint_line(x - 30, y, x + 30, y)  # Horizontal line
    draw_midpoint_line(x - 30, y, x - 30, y + 20)  # Left vertical line
    draw_midpoint_line(x + 30, y, x + 30, y + 20)  # Right vertical line
    draw_midpoint_line(x - 30, y + 20, x + 30, y + 20)  # Bottom horizontal line

def draw_diamond():
    x, y = diamond_pos
    color = (random.random(), random.random(), random.random())
    glColor3f(*color)
    # Diamond shape using midpoint lines
    draw_midpoint_line(x + 10, y + 20, x + 30, y + 10)  # Right diagonal
    draw_midpoint_line(x + 30, y + 10, x + 10, y)  # Bottom diagonal
    draw_midpoint_line(x + 10, y, x - 10, y + 10)  # Left diagonal
    draw_midpoint_line(x - 10, y + 10, x + 10, y + 20)  # Top diagonal

def draw_buttons():
    # Rectangle bounds for buttons
    button_width, button_height = BUTTON_WIDTH, BUTTON_HEIGHT

    # Restart button
    restart_x, restart_y = 50, HEIGHT - button_height - 50
    glColor3f(*TEAL)
    draw_arrow(restart_x + button_width // 2, restart_y + button_height // 2, 'left', BUTTON_WIDTH)

    # Play/Pause button
    play_pause_x, play_pause_y = 50 + button_width + BUTTON_PADDING, HEIGHT - button_height - 50
    glColor3f(*AMBER)
    draw_play_pause(play_pause_x + button_width // 2, play_pause_y + button_height // 2, BUTTON_WIDTH)

    # Quit button
    quit_x, quit_y = play_pause_x + button_width + BUTTON_PADDING, HEIGHT - button_height - 50
    glColor3f(*RED)
    draw_cross(quit_x + button_width // 2, quit_y + button_height // 2, BUTTON_WIDTH)

def draw_arrow(x, y, direction, size):
    scale = size / 60  # Scale the drawing
    if direction == 'left':
        draw_midpoint_line(x - 20 * scale, y - 10 * scale, x - 30 * scale, y)  # Left
        draw_midpoint_line(x - 20 * scale, y + 10 * scale, x - 30 * scale, y)  # Right
        draw_midpoint_line(x - 30 * scale, y, x - 20 * scale, y)  # Base

def draw_play_pause(x, y, size):
    scale = size / 60  # Scale the drawing
    if game_state == 'playing':
        draw_midpoint_line(x - 5 * scale, y + 10 * scale, x + 5 * scale, y + 10 * scale)  # Horizontal line
        draw_midpoint_line(x - 5 * scale, y - 10 * scale, x + 5 * scale, y - 10 * scale)  # Horizontal line
    else:
        draw_midpoint_line(x - 10 * scale, y + 10 * scale, x + 10 * scale, y)  # Triangle 1
        draw_midpoint_line(x - 10 * scale, y - 10 * scale, x + 10 * scale, y)  # Triangle 2

def draw_cross(x, y, size):
    scale = size / 60  # Scale the drawing
    draw_midpoint_line(x - 10 * scale, y - 10 * scale, x + 10 * scale, y + 10 * scale)  # Diagonal lines
    draw_midpoint_line(x - 10 * scale, y + 10 * scale, x + 10 * scale, y - 10 * scale)  # Diagonal lines

def update(value):
    global last_time, delta_time, diamond_speed, diamond_pos, score, game_state

    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    if game_state == 'playing':
        diamond_pos[1] -= diamond_speed * delta_time

        # Check for collision with catcher
        if has_collided(diamond_pos, [catcher_pos - 30, 50, 60, 20]):
            score += 1
            diamond_pos = [random.randint(0, WIDTH - 20), HEIGHT]
            diamond_speed += 10  # Increase speed with each caught diamond
            print(f"Score: {score}, Speed: {diamond_speed}")

        # Check if diamond hits the ground
        if diamond_pos[1] <= 0:
            game_state = 'game over'
            print(f"Game Over! Score: {score}")

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    draw_catcher()
    draw_diamond()
    draw_buttons()
    glutSwapBuffers()

def keyboard(key, x, y):
    global catcher_pos
    if game_state == 'playing':
        catcher_width = 60  # Width of the catcher

        if key == GLUT_KEY_LEFT:
            # Move left but ensure it doesn't go out of bounds
            catcher_pos = max(catcher_width // 2, catcher_pos - 10)
        elif key == GLUT_KEY_RIGHT:
            # Move right but ensure it doesn't go out of bounds
            catcher_pos = min(WIDTH - catcher_width // 2, catcher_pos + 10)


def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        handle_button_click(x, HEIGHT - y)

def handle_button_click(x, y):
    global game_state, score, diamond_speed, catcher_pos, diamond_pos

    # Rectangle bounds for each button
    button_width, button_height = BUTTON_WIDTH, BUTTON_HEIGHT

    # Restart button rectangle
    restart_x, restart_y = 50, HEIGHT - button_height - 50
    if restart_x <= x <= restart_x + button_width and \
       restart_y <= y <= restart_y + button_height:
        game_state = 'playing'
        score = 0
        diamond_speed = 150  # Reset speed to original value
        catcher_pos = WIDTH // 2
        diamond_pos = [random.randint(0, WIDTH - 20), HEIGHT]
        print("Starting Over")

    # Play/Pause button rectangle
    play_pause_x, play_pause_y = 50 + button_width + BUTTON_PADDING, HEIGHT - button_height - 50
    if play_pause_x <= x <= play_pause_x + button_width and \
       play_pause_y <= y <= play_pause_y + button_height:
        if game_state == 'playing':
            game_state = 'paused'
        elif game_state == 'paused':
            game_state = 'playing'

    # Quit button rectangle
    quit_x, quit_y = play_pause_x + button_width + BUTTON_PADDING, HEIGHT - button_height - 50
    if quit_x <= x <= quit_x + button_width and \
       quit_y <= y <= quit_y + button_height:
        print(f"Goodbye! Score: {score}")
        glutLeaveMainLoop()


def has_collided(diamond, catcher):
    return (diamond[0] < catcher[0] + catcher[2] and
            diamond[0] + 20 > catcher[0] and
            diamond[1] < catcher[1] + catcher[3] and
            diamond[1] + 20 > catcher[1])

glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WIDTH, HEIGHT)
glutCreateWindow(b"Catch the Diamonds!")
init()
glutDisplayFunc(display)
glutSpecialFunc(keyboard)
glutMouseFunc(mouse)
glutTimerFunc(16, update, 0)
glutMainLoop()
