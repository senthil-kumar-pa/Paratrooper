import pyglet
import random
import math
from pyglet import shapes
from pyglet.window import key
from pyglet.sprite import Sprite

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_ROTATION_STEP = 5
BULLET_SPEED = 10
PARATROOPER_SPEED = 2
PARATROOPER_SPAWN_RATE = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
PINK = (255, 192, 203)

# Setup Pyglet window
window = pyglet.window.Window(WIDTH, HEIGHT, "Paratrooper Game")

key_handler = key.KeyStateHandler()
window.push_handlers(key_handler)

batch = pyglet.graphics.Batch()

score_label = pyglet.text.Label(
    "Score: 0", 
    font_name="Arial", 
    font_size=20, 
    x=WIDTH - 100, y=HEIGHT - 30,  # Top right position
    anchor_x="right", anchor_y="top",
    color=(255, 255, 255, 255)  # White color
)


# Load assets
player_image = pyglet.image.load("player.png")
paratrooper_image = pyglet.image.load("paratrooper.png")
landed_paratrooper_image = pyglet.image.load("landedparatrooper.png")
bullet_image = pyglet.image.load("bullet.png")

# Sounds (using pyglet's load method for mp3)
shoot_sound = pyglet.media.load("shoot.mp3", streaming=False)
hit_sound = pyglet.media.load("hit.mp3", streaming=False)

# Global variables for game state
player = None
bullets = []
paratroopers = []  # Initialize paratroopers list here
landed_paratroopers = 0
frame_count = 0
score = 0  # Initialize score


# Classes
class Player:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = 65  # Position the player at the bottom of the screen
        self.width = 25
        self.height = 25
        self.angle = 90  # Start facing upward
        player_image.anchor_x = player_image.width // 2
        player_image.anchor_y = player_image.height // 2
        self.sprite = pyglet.sprite.Sprite(player_image, self.x, self.y, batch=batch)
        # Update the position to be the center of the sprite (center of rotation)
        # Set rotation anchor to the center of the image

    def rotate(self, direction):
        if direction == "right" and self.angle > 0:
            self.angle -= PLAYER_ROTATION_STEP  # Decrease for left
        if direction == "left" and self.angle < 180:
            self.angle += PLAYER_ROTATION_STEP  # Increase for right

        self.sprite.rotation = -self.angle + 90  # Negate the angle for correct rotation

class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.width = 10
        self.height = 20
        self.angle = math.radians(angle)  # Convert to radians
        self.dx = BULLET_SPEED * math.cos(self.angle)
        self.dy = BULLET_SPEED * math.sin(self.angle)  # Fix bullet direction to go upwards
        self.sprite = pyglet.sprite.Sprite(bullet_image, self.x, self.y, batch=batch)

    def move(self):
        self.x += self.dx
        self.y += self.dy
        self.sprite.update(x=self.x, y=self.y)

    def draw(self):
        self.sprite.draw()

class Paratrooper:
    def __init__(self):
        self.x = random.randint(0, WIDTH - 50)
        self.y = HEIGHT  # Start paratroopers from the top
        self.width = 40
        self.height = 40
        self.landed = 0
        self.sprite = pyglet.sprite.Sprite(paratrooper_image, self.x, self.y, batch=batch)

    def move(self):
        self.y -= PARATROOPER_SPEED  # Move paratrooper down
        self.sprite.update(x=self.x, y=self.y)

    def draw(self):
        if self.landed:
            self.sprite.image = landed_paratrooper_image
        self.sprite.draw()

# Game setup
player = Player()

# Game loop
@window.event
def on_draw():
    window.clear()
    batch.draw()
    score_label.draw()
ROTATION_SPEED = 100  # Degrees per second

# Update logic for game state
def update(dt):
    global landed_paratroopers, frame_count, paratroopers  

    # Continuous rotation based on key state
    if key_handler[key.LEFT]:
        player.angle += ROTATION_SPEED * dt
    if key_handler[key.RIGHT]:
        player.angle -= ROTATION_SPEED * dt

    player.sprite.rotation = -player.angle + 90

    if key_handler[key.ESCAPE]:  # Move ESC logic here
        pyglet.app.exit()
    if key_handler[key.SPACE]:
        shoot_sound.play()
        
        # Convert angle to radians
        angle_rad = math.radians(player.angle)
        
        # Calculate bullet start position at the top middle of the turret
        bullet_x = player.x + math.cos(angle_rad) * (player.sprite.height / 2)
        bullet_y = player.y + math.sin(angle_rad) * (player.sprite.height / 2)
        
        # Create bullet and add to list
        bullets.append(Bullet(bullet_x, bullet_y, player.angle))


    # Handle bullet movement and collision
    # Handle bullet movement and collision
    for bullet in bullets[:]:
        bullet.move()
        for para in paratroopers[:]:
            if (bullet.x < para.x + para.width and
                bullet.x + bullet.width > para.x and
                bullet.y < para.y + para.height and
                bullet.y + bullet.height > para.y):
                
                bullets.remove(bullet)
                paratroopers.remove(para)
                hit_sound.play()
                
                global score
                score += 100  # Increase score
                score_label.text = f"Score: {score}"  # Update label text
                
                break  # Stop checking after a hit


    # Add new paratroopers
    if frame_count % PARATROOPER_SPAWN_RATE == 0:
        paratroopers.append(Paratrooper())

    # Move paratroopers and check landing
    for para in paratroopers[:]:
        if para.landed == 0:
            para.move()
        if para.y <= 0 and para.landed == 0:  
            landed_paratroopers += 1
            para.landed = 1

    paratroopers = [p for p in paratroopers if p.y > 0]

    # Change background color based on landed paratroopers
    if landed_paratroopers > 100:
        pyglet.gl.glClearColor(1, 0, 0, 1)
        print("GAME OVER")
        pyglet.app.exit()
    elif landed_paratroopers > 5:
        pyglet.gl.glClearColor(1, 0.75, 0.8, 1)
    else:
        pyglet.gl.glClearColor(0, 0, 0, 1)

    frame_count += 1



# Set the update function to be called at regular intervals
pyglet.clock.schedule_interval(update, 1/60.0)

# Start the game
pyglet.app.run()
