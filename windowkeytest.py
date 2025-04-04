import pyglet
from pyglet.window import key

# Window setup
WIDTH, HEIGHT = 800, 600
window = pyglet.window.Window(WIDTH, HEIGHT, "Turret Rotation Test")

# Load turret image
turret_image = pyglet.image.load("player.png")  # Ensure you have this image
turret_image.anchor_x = turret_image.width // 2  # Center anchor
turret_image.anchor_y = turret_image.height // 2

# Create turret sprite
turret = pyglet.sprite.Sprite(turret_image, x=WIDTH//2, y=HEIGHT//2)

# Key state handler
key_handler = key.KeyStateHandler()
window.push_handlers(key_handler)

# Rotation step
ROTATION_SPEED = 100  # Degrees per second

# Update function
def update(dt):
    if key_handler[key.LEFT]:
        turret.rotation += ROTATION_SPEED * dt  # Rotate left
    if key_handler[key.RIGHT]:
        turret.rotation -= ROTATION_SPEED * dt  # Rotate right

# Draw function
@window.event
def on_draw():
    window.clear()
    turret.draw()

# Schedule update function
pyglet.clock.schedule_interval(update, 1/60.0)  # Runs at 60 FPS

# Start game loop
pyglet.app.run()
