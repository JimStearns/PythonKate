# Implementation of classic arcade game Pong
# Kate's implementation as of 30-Oct-2014
# Initially dependent on CodeSkulptor and simplegui.
# Plan: move to standard python, with the most commonly used GUI package: Tkinter.

# Program was designed to run using class's CodeSkulptor.
#   To get running in regular Python takes a little work: this simplegui package won't install.
#   See http://stackoverflow.com/questions/16387770/how-to-integrate-simplegui-with-python-2-7-and-3-0-shell
#   for details.
#
# Kate Stearns original code can be found here:
#   http://www.codeskulptor.org/#user38_iBHnqdemd5JlrNI_6.py

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
CENTER_COURT = [WIDTH / 2, HEIGHT / 2]
INITIAL_POS_RED_PAD = [1, (HEIGHT /2) - (PAD_HEIGHT / 2)]
INITIAL_POS_BLUE_PAD = [(WIDTH - 1) , (HEIGHT /2) - (PAD_HEIGHT / 2)]
TIMER_INTERVAL_MS = 50
MS_PER_SECOND = 1000
paddle_red_vel = [0,4]
paddle_blue_vel = [0,4]

# For readability: which element in the list is X, and which is Y?
X = 0
Y = 1

#Coordinates of Paddles are upper left of corner

# initialize ball_pos and ball_vel for new bal in middle of table
# if general direction is RIGHT, default direction is to the UPPER RIGHT, else UPPER LEFT.
def spawn_ball(direction):
    global ball_pos, ball_vel 
    ball_pos = CENTER_COURT
    if direction == RIGHT:
        ball_vel = [180, -90]	# Positive movement along x-axis. No change in y.
    else:
        ball_vel = [-180, -90] # Negative movement in x-axis. No change in y.


# define event handlers
def new_game():
    global paddle_red_pos, paddle_blue_pos, paddle_red_vel, paddle_blue_vel  # these are numbers
    global score1, score2  # these are ints
    paddle_red_pos = INITIAL_POS_RED_PAD
    paddle_blue_pos = INITIAL_POS_BLUE_PAD
    direction = RIGHT 
    spawn_ball(direction)

def draw(canvas):
    global score1, score2, paddle_red_pos, paddle_blue_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 2, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 2, "Red")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 2, "Cyan")
            
    # draw ball 
    canvas.draw_circle(ball_pos, BALL_RADIUS, 12, "White", "White")
    
    # draw paddles
    draw_red_paddle(canvas)
    canvas.draw_line(paddle_blue_pos, [paddle_blue_pos[0], paddle_blue_pos[1] + PAD_HEIGHT], PAD_WIDTH, "Cyan")
    
    # draw scores
    canvas.draw_text("0", [WIDTH / 1.4, HEIGHT / 4], 40, "Cyan")
    canvas.draw_text("0", [WIDTH / 4, HEIGHT / 4], 40, "Red")

def ball_hitting_side():
    if ball_pos[Y] < BALL_RADIUS and ball_vel[Y] < 0:
        return(True)
    elif (ball_pos[Y] + BALL_RADIUS) >= HEIGHT and ball_vel[Y] > 0:
        return(True)
 
    return(False)

def ball_hitting_goal():
    if ball_pos[X] < BALL_RADIUS and ball_vel[X] < 0:
        return(True)
    elif (ball_pos[X] + BALL_RADIUS) >= WIDTH and ball_vel[X] > 0:
        return(True)
 
    return(False)

def paddle_in_way():
    if (ball_pos[X] + BALL_RADIUS) == paddle_red_pos[X]:
        return(True)
    elif (ball_pos[Y] + BALL_RADIUS) == paddle_red_pos[Y]:
        return (True)
        
    # For now, always return TRUE
    # TBD: Calculate paddle position relative to ball.
    return(True)

def timer_handler():
    #print "tick"
    
    # Update direction of velocity if in contact with side(line) or goal(line)
    if ball_hitting_goal():
        if paddle_in_way():
            ball_vel[X] = -ball_vel[X]
            print "Hit Goal, velocity is now", ball_vel
        else:
            print("Game Over")
            # Stop timer (so ball stops)
            
            # Say who won.
            
    if ball_hitting_side():
        ball_vel[Y] = -ball_vel[Y]
        #ball_vel[X] = -ball_vel[X]
    
    # Update ball position using velocity (units: pixels per second)
    ball_pos[X] += ball_vel[X] * TIMER_INTERVAL_MS / MS_PER_SECOND
    ball_pos[Y] += ball_vel[Y] * TIMER_INTERVAL_MS / MS_PER_SECOND
    
    # TODO: Change (increase) velocity to keep game interesting.

timer = simplegui.create_timer(100, timer_handler)
    
def draw_red_paddle(canvas):
    canvas.draw_line(paddle_red_pos, [paddle_red_pos[0], paddle_red_pos[1] + PAD_HEIGHT], PAD_WIDTH,"Red")

def draw_blue_paddle(canvas):
    canvas.draw_line(paddle_blue_pos, [paddle_blue_pos[0], paddle_blue_pos[1] + PAD_HEIGHT], PAD_WIDTH, "Cyan")
 
def draw_ball(canvas):    
    canvas.draw_circle(ball_pos, BALL_RADIUS, 12, "White", "White")
    
def draw_score_red(canvas):
    # Red team score
    canvas.draw_text("0", [WIDTH / 4, HEIGHT / 4], 40, "Red")
    # Blue team score
    
def draw_score_blue(canvas):    
    canvas.draw_text("0", [WIDTH / 1.4, HEIGHT / 4], 40, "Cyan")
    
def keydown(key):
    global paddle_red_vel, paddle_blue_vel, paddle_red_pos
    if key == simplegui.KEY_MAP["w"]:
        print "up"
        paddle_red_pos[1] -= HEIGHT / 20
        if paddle_red_pos[1] < 0:
            paddle_red_pos[1] = 0
    elif key == simplegui.KEY_MAP["up"]:
        print "up"
        paddle_blue_pos[1] -= HEIGHT / 20
        if paddle_blue_pos[1] < 0:
            paddle_blue_pos[1] = 0
    elif key == simplegui.KEY_MAP["s"]:
        print "down"
        paddle_red_pos[1] += HEIGHT / 20
        if paddle_red_pos[1] > HEIGHT - PAD_HEIGHT:
            paddle_red_pos[1] = HEIGHT - PAD_HEIGHT
    elif key == simplegui.KEY_MAP["down"]:
        print "down"
        paddle_blue_pos[1] += HEIGHT / 20
        if paddle_blue_pos[1] > HEIGHT - PAD_HEIGHT:
            paddle_blue_pos[1] = HEIGHT - PAD_HEIGHT
        
        
   
def keyup(key):
    global paddle_red_vel, paddle_blue_vel


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)

# Create the timer to handle changes in ball position and velocity.
timer = simplegui.create_timer(TIMER_INTERVAL_MS, timer_handler)


# start frame
new_game()
frame.start()
timer.start()

# Questions for Dad
# Do i need to make a function to get the ball to move on the y axis?
#How will I get the score to update?
# What do you think of the colors?