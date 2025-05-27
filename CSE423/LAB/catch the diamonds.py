from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import random
import time

# Screen dimensions
WIDTH, HEIGHT = 800, 800 #550,650

# Game variables
catcher_pos = WIDTH // 2
diamond_pos = [random.randint(40, WIDTH - 40), HEIGHT]
diamond_speed = 150  # Starting speed
score = 0
game_state = 'playing'
diamond_color = (1.0, 1.0, 1.0)  # Default color
quit_flag = False  # Flag to indicate game should quit

# Colors
white = (1.0, 1.0, 1.0)
red = (1.0, 0.0, 0.0)
teal = (0.0, 1.0, 1.0)
amber = (1.0, 0.75, 0.0)
background = (0.0, 0.0, 0.0)

# Time variables for delta timing
last_time = time.time()
delta_time = 0

# Button dimensions
button_width, button_height = 120, 200  # Increased button size
button_padding = 10  # Adjust padding accordingly

# Adjusted sizes for better collision detection
catcher_width, catcher_height = 60, 20
diamond_width, diamond_height = 20, 20

def init():
    glClearColor(*background, 1.0)
    gluOrtho2D(0, WIDTH, 0, HEIGHT)

def find_zone(x1, y1, x2, y2):
    dy = y2 - y1
    dx = x2 - x1
    if abs(dy) > abs(dx):
        if dy >= 0 and dx >= 0:
            return 1
        elif dy >= 0 and dx <= 0:
            return 2
        elif dy <= 0 and dx <= 0:
            return 5
        elif dy <= 0 and dx >= 0:
            return 6
    else:
        if dy >= 0 and dx >= 0:
            return 0
        elif dy >= 0 and dx <= 0:
            return 3
        elif dy <= 0 and dx <= 0:
            return 4
        elif dy <= 0 and dx >= 0:
            return 7

def eight_way_other_to_zero(x1, y1, x2, y2, zone):
    if zone == 1:
        return y1, x1, y2, x2
    elif zone == 2:
        return y1, -x1, y2, -x2
    elif zone == 3:
        return -x1, y1, -x2, y2
    elif zone == 4:
        return -x1, -y1, -x2, -y2
    elif zone == 5:
        return -y1, -x1, -y2, -x2
    elif zone == 6:
        return -y1, x1, -y2, x2
    elif zone == 7:
        return x1, -y1, x2, -y2
    return x1, y1, x2, y2

def eight_way_zero_to_other(x, y, zone):
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return -y, x
    elif zone == 3:
        return -x, y
    elif zone == 4:
        return -x, -y
    elif zone == 5:
        return -y, -x
    elif zone == 6:
        return y, -x
    elif zone == 7:
        return x, -y

def draw_midpoint_line(x1, y1, x2, y2):
    zone = find_zone(x1, y1, x2, y2)
    x1_0, y1_0, x2_0, y2_0 = eight_way_other_to_zero(x1, y1, x2, y2, zone)
    
    dx = x2_0 - x1_0
    dy = y2_0 - y1_0
    d = 2 * dy - dx
    dE = 2 * dy
    dNE = 2 * (dy - dx)
    x = x1_0
    y = y1_0
    glPointSize(2)
    glBegin(GL_POINTS)
    while x <= x2_0:
        a, b = eight_way_zero_to_other(x, y, zone)
        glVertex2f(a, b)
        if d < 0:
            x += 1
            d += dE
        else:
            x += 1
            y += 1
            d += dNE
    glEnd()


def draw_catcher():
    x = catcher_pos
    y = 50
    color = white if game_state != 'game over' else red
    glColor3f(*color)
    draw_midpoint_line((x - catcher_width // 2), y, (x + catcher_width // 2), y)  # Horizontal line
    draw_midpoint_line(x - catcher_width // 2, y, (x - catcher_width // 2)-10, y + catcher_height)  # Left vertical line
    draw_midpoint_line(x + catcher_width // 2, y, (x + catcher_width // 2)+10, y + catcher_height)  # Right vertical line
    draw_midpoint_line((x - catcher_width // 2)-10, y + catcher_height, (x + catcher_width // 2)+10, y + catcher_height)  # Bottom horizontal line

def draw_diamond():
    x, y = diamond_pos
    glColor3f(*diamond_color)  # Ensure diamond color is applied
    # Diamond shape using midpoint lines (rotated 90 degrees clockwise)
    draw_midpoint_line(x + diamond_height // 2, y, x, y - diamond_width // 2)  # Right diagonal
    draw_midpoint_line(x, y - diamond_width // 2, x - diamond_height // 2, y)  # Bottom diagonal
    draw_midpoint_line(x - diamond_height // 2, y, x, y + diamond_width // 2) # Left diagonal
    draw_midpoint_line(x, y + diamond_width // 2, x + diamond_height // 2, y)  # Top diagonal

def draw_buttons():
    btn_width, btn_height = button_width, button_height

    # Adjusting y position to move buttons higher
    vertical_offset = 70

    # Left Corner (Restart button)
    restart_x, restart_y = 50, HEIGHT - btn_height - 50 + vertical_offset
    glColor3f(*teal)
    draw_arrow(restart_x + btn_width // 2, restart_y + btn_height // 2, 'left', button_width)

    # Middle (Play/Pause button)
    play_pause_x = WIDTH // 2 - btn_width // 2
    play_pause_y = HEIGHT - btn_height - 50 + vertical_offset
    glColor3f(*amber)
    draw_play_pause(play_pause_x + btn_width // 2, play_pause_y + btn_height // 2, button_width)

    # Right Corner (Quit button)
    quit_x = WIDTH - btn_width - 50
    quit_y = HEIGHT - btn_height - 50 + vertical_offset
    glColor3f(*red)
    draw_cross(quit_x + btn_width // 2, quit_y + btn_height // 2, button_width)

def draw_arrow(x, y, direction, size):
    scale = size / 60
    if direction == 'left':
        draw_midpoint_line(x - 20 * scale, y - 10 * scale, x - 30 * scale, y)  # Left
        draw_midpoint_line(x - 20 * scale, y + 10 * scale, x - 30 * scale, y)  # Right
        draw_midpoint_line(x - 30 * scale, y, x -10 * scale, y)  # Base

def draw_play_pause(x, y, size):
    scale = size / 60
    if game_state == 'playing':
        draw_midpoint_line(x - 10 * scale, y + 5 * scale, x - 10 * scale, y - 10 * scale)  # Left vertical line
        draw_midpoint_line(x + 10 * scale, y + 5 * scale, x + 10 * scale, y - 10 * scale)  # Right vertical line
    else:
        draw_midpoint_line(x - 10 * scale, y + 10 * scale, x + 10 * scale, y)  # Triangle 1
        draw_midpoint_line(x - 10 * scale, y - 10 * scale, x + 10 * scale, y)  # Triangle 2
        draw_midpoint_line(x - 10 * scale,  y + 10 * scale, x - 10 * scale, y - 10 * scale)

def draw_cross(x, y, size):
    scale = size / 60
    draw_midpoint_line(x - 10 * scale, y - 10 * scale, x + 10 * scale, y + 10 * scale)  # Diagonal lines
    draw_midpoint_line(x - 10 * scale, y + 10 * scale, x + 10 * scale, y - 10 * scale)  # Diagonal lines

def update(value):
    global last_time, delta_time, diamond_speed, diamond_pos, score, game_state, quit_flag, diamond_color

    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time

    if game_state == 'playing':
        diamond_pos[1] -= diamond_speed * delta_time
        catcher_rect = [
            catcher_pos - catcher_width // 2 - 10,
            50,
            catcher_width + 20,
            catcher_height
        ]
        diamond_rect = [
            diamond_pos[0] - diamond_width // 2,
            diamond_pos[1] - diamond_height // 2,
            diamond_width,
            diamond_height
        ]

        if has_collided(diamond_rect, catcher_rect):
            score += 1
            diamond_pos = [random.randint(0, WIDTH - diamond_width), HEIGHT]
            diamond_speed += 10  # Increase speed with each caught diamond
            diamond_color = generate_diamond_color()  # Change diamond color
            print(f"Score: {score}, Speed: {diamond_speed}")

        if diamond_pos[1] <= 0:
            game_state = 'game over'
            print(f"Game Over! Score: {score}")

    if quit_flag:
        print("Goodbye")
        glutLeaveMainLoop()  # Exit the GLUT main loop

    glutPostRedisplay()
    glutTimerFunc(25, update, 0)

def display():
    glClear(GL_COLOR_BUFFER_BIT)

    draw_catcher()
    draw_diamond()
    draw_buttons()

    glutSwapBuffers()

def keyboard(key, x, y):
    global quit_flag
    if key == b'\x1b':  # Escape key
        quit_flag = True

def special_keyboard(key, x, y):
    global catcher_pos
    if game_state != 'game over':
        if key == GLUT_KEY_LEFT:
            catcher_pos -= 10
            if catcher_pos - catcher_width // 2 - 10 < 0:
                catcher_pos = catcher_width // 2 + 10
        elif key == GLUT_KEY_RIGHT:
            catcher_pos += 10
            if catcher_pos + catcher_width // 2 + 10 > WIDTH:
                catcher_pos = WIDTH - catcher_width // 2 - 10


def mouse(button, state, x, y):
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        handle_button_click(x, HEIGHT - y)

def handle_button_click(x, y):
    global game_state, diamond_pos, diamond_speed, score, diamond_color, quit_flag
    btn_width, btn_height = button_width, button_height

    # Adjusting y position to match buttons being higher
    vertical_offset = 70

    # Left Corner (Restart button)
    restart_x, restart_y = 50, HEIGHT - btn_height - 50 + vertical_offset
    if restart_x <= x <= restart_x + btn_width and restart_y <= y <= restart_y + btn_height:
        game_state = 'playing'
        diamond_pos = [random.randint(0, WIDTH - diamond_width), HEIGHT]
        diamond_speed = 150
        score = 0
        diamond_color = (1.0, 1.0, 1.0)
        return

    # Middle (Play/Pause button)
    play_pause_x = WIDTH // 2 - btn_width // 2
    play_pause_y = HEIGHT - btn_height - 50 + vertical_offset
    if play_pause_x <= x <= play_pause_x + btn_width and play_pause_y <= y <= play_pause_y + btn_height:
        if game_state == 'playing':
            game_state = 'paused'
        elif game_state == 'paused':
            game_state = 'playing'
        return

    # Right Corner (Quit button)
    quit_x = WIDTH - btn_width - 50
    quit_y = HEIGHT - btn_height - 50 + vertical_offset
    if quit_x <= x <= quit_x + btn_width and quit_y <= y <= quit_y + btn_height:
        quit_flag = True
        return

def has_collided(diamond_rect, catcher_rect):
    # Diamond rectangle coordinates
    diamond_left = diamond_rect[0]
    diamond_right = diamond_rect[0] + diamond_rect[2]
    diamond_top = diamond_rect[1]
    diamond_bottom = diamond_rect[1] - diamond_rect[3]

    # Catcher rectangle coordinates
    catcher_left = catcher_rect[0]
    catcher_right = catcher_rect[0] + catcher_rect[2]
    catcher_top = catcher_rect[1]
    catcher_bottom = catcher_rect[1] - catcher_rect[3]

    # AABB collision detection logic
    return (diamond_left < catcher_right and
            diamond_right > catcher_left and
            diamond_top > catcher_bottom and
            diamond_bottom < catcher_top)

def generate_diamond_color():
    while True:
        color = (random.random(), random.random(), random.random())
        # Ensure the color is not too close to the background
        if not is_similar(color, background, 0.2):
            return color

def is_similar(color1, color2, threshold):
    return (abs(color1[0] - color2[0]) < threshold and
            abs(color1[1] - color2[1]) < threshold and
            abs(color1[2] - color2[2]) < threshold)


glutInit()
glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB)
glutInitWindowSize(WIDTH, HEIGHT)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"Diamond Catcher Game")

init()
glutDisplayFunc(display)
glutKeyboardFunc(keyboard)
glutSpecialFunc(special_keyboard)
glutMouseFunc(mouse)
glutTimerFunc(25, update, 0)

glutMainLoop()
