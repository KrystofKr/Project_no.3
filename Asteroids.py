import pyglet

import random
from math import cos,sin, degrees
from PIL import Image


batch = pyglet.graphics.Batch()

ROTATION_SPEED = 3
ACCELERATION = 20
ASTEROID_SPEED = 100
ASTEROID_ROTATION_SPEED = 5
LASER_SPEED = 500
SHOOT_INTERVAL = 0.5

pressed_keys = set()
game_active = False

def load_image(image):
    image_done = pyglet.image.load(image)
    image_done.anchor_x = image_done.width//2
    image_done.anchor_y = image_done.height//2
    return image_done

window = pyglet.window.Window(width=1000,height = 800)

#images
image = load_image("PNG/playerShip1_blue.png")
asteroid_image = load_image("PNG/Meteors/meteorBrown_big1.png")
laser_image = load_image("PNG/Lasers/laserBlue01.png")
#resize
background_resize = Image.open("Backgrounds/black.png")
new_resize = background_resize.resize((1000,800))
new_resize.save("black_resize.png")
#background
background = load_image("Backgrounds/black_resize.png")
background_sprite = pyglet.sprite.Sprite(background)

#audio
laser_audio = pyglet.media.load("Bonus/sfx_laser1.ogg", streaming=False)

#background
bg_audio = pyglet.media.load("Backgrounds/A Journey Awaits.mp3")
bg_audio.loop = True

while game_active:
    bg_audio.play()


def distance(a, b, wrap_size):
    """Distance in one direction (x or y)"""
    result = abs(a - b)
    if result > wrap_size / 2:
        result = wrap_size - result
    return result

def overlaps(a, b):
    """Returns true iff two space objects overlap"""
    distance_squared = (distance(a.x, b.x, window.width) ** 2 +
                        distance(a.y, b.y, window.height) ** 2)
    max_distance_squared = (a.radius + b.radius) ** 2
    return distance_squared < max_distance_squared

class Spaceobject:
    def __init__(self,image):
        self.x = 0
        self.y = 0
        self.speed_x = 0
        self.speed_y = 0
        self.rotation = 0
        self.rotation_speed = 0
        self.radius = 30

        self.sprite = pyglet.sprite.Sprite(image)

    def draw(self):
        self.sprite.x = self.x
        self.sprite.y = self.y
        self.sprite.rotation = 90 - degrees(self.rotation)
        self.sprite.draw()

    def tick(self,t):
        self.y += self.speed_y * t
        self.x += self.speed_x * t
        self.rotation += self.rotation_speed * t
        self.x = self.x % window.width
        self.y = self.y % window.height

    def delete(self):
        try:
            object.remove(self)
        except ValueError:
            pass
    
    def hit_by_spaceship(self, ship):
        pass

    def hit_by_laser(self, ship):
        pass

class SpaceShip(Spaceobject):
    def __init__(self):
        super().__init__(image)
        bg_audio.play()
        self.x = window.width/2
        self.y = window.height/2
        self.next_fire = 0
 


    def tick(self,t):
        super().tick(t)
        if pyglet.window.key.LEFT in pressed_keys:
            self.rotation += ROTATION_SPEED * t
        if pyglet.window.key.RIGHT in pressed_keys:
            self.rotation -= ROTATION_SPEED * t
        if pyglet.window.key.UP in pressed_keys:
            self.speed_x  += ACCELERATION * cos(self.rotation)
            self.speed_y  += ACCELERATION * sin(self.rotation)
        if pyglet.window.key.SPACE in pressed_keys and self.next_fire <=0:
            laser = Laser(ship)
            object.append(laser)
            self.next_fire = SHOOT_INTERVAL
        self.next_fire -= t
        
        for obj in list(object):
            if overlaps(self,obj):
                obj.hit_by_spaceship(self)

class Laser(Spaceobject):
    def __init__(self, ship):
        
        laser_audio.play()
        super().__init__(laser_image)
        self.x = ship.x
        self.y = ship.y
        self.rotation = ship.rotation
        self.radius = 20
        self.speed_x  += LASER_SPEED * cos(self.rotation)
        self.speed_y  += LASER_SPEED * sin(self.rotation)  

    def tick(self,t):
        super().tick(t)
        for obj in list(object):
            if overlaps(self,obj):
                obj.hit_by_laser(self)

class Asteroid(Spaceobject):
    def __init__(self, size):
        if size == 4:
            ast_size = "big"
            radius = 40
        elif size == 3:
            ast_size = "med"
            radius = 20
        elif size == 2:
            ast_size = "small"
            radius = 10
        elif size == 1:
            ast_size = "tiny"
            radius = 5
        else:
            size = 0
            
        self.size = size-1
        image = load_image(f"PNG/Meteors/meteorBrown_{ast_size}1.png")
        super().__init__(image)
        self.x = random.uniform(0,window.width)
        self.speed_x = random.uniform(-ASTEROID_SPEED,ASTEROID_SPEED)
        self.speed_y = random.uniform(-ASTEROID_SPEED,ASTEROID_SPEED)
        self.rotation_speed = random.uniform(-ASTEROID_ROTATION_SPEED,ASTEROID_ROTATION_SPEED)
        self.radius = 40

    
    def hit_by_spaceship(self, ship):
        ship.delete()
    def hit_by_laser(self, laser):
        self.delete()
        laser.delete()

        if self.size > 0:
            for i in range(2):
                new_asteroid = Asteroid(self.size)
                new_asteroid.x = self.x
                new_asteroid.y = self.y
                new_asteroid.speed_x += random.uniform(-ASTEROID_SPEED,ASTEROID_SPEED)
                new_asteroid.speed_y += random.uniform(-ASTEROID_SPEED,ASTEROID_SPEED)
                object.append(new_asteroid)

ship = SpaceShip()

def tick(t):
    for obj in object:
        obj.tick(t)

pyglet.clock.schedule_interval(tick, 1/30)

object =[ship, Asteroid(4), Asteroid(4), Asteroid(4)]

def menu():
        global game_active
        button_image = load_image("PNG/UI/buttonBlue.png")
        button_sprite = pyglet.sprite.Sprite(button_image, batch = batch)
        button_sprite.x = window.width // 2
        button_sprite.y = window.height // 2
        pyglet.font.add_file("Bonus/kenvector_future.ttf")
        pyglet.font.add_file("Bonus/kenvector_future_thin.ttf")
        start_label = pyglet.text.Label("Start",
                                  x=button_sprite.x,
                                  y=button_sprite.y,
                                  color= (0,0,0,255),
                                  batch=batch, 
                                  font_name= "kenvector future", 
                                  font_size= 20, 
                                  anchor_x="center",
                                  anchor_y="center")
        name_label = pyglet.text.Label("ASTEROIDS",
                                       x = button_sprite.x,
                                       y = button_sprite.y + 200,
                                       color= (255,255,255,255),
                                       batch=batch,
                                       font_name= "kenvector future",
                                       font_size= 60,
                                       anchor_x="center",
                                       anchor_y="center")
        if pyglet.window.key.SPACE in pressed_keys:
            game_active = True
        #print(pyglet.font.have_font)
        batch.draw()


@window.event
def on_draw():
    if game_active:
        
        window.clear() # začetnění okénka
        background_sprite.x =window.width/2
        background_sprite.y =window.height/2
        background_sprite.draw()
        for obj in object:
            obj.draw()
    if not game_active:
        window.clear()
        menu()
        



@window.event
def on_key_press(key, mod):
    pressed_keys.add(key)

@window.event
def on_key_release(key, mod):
    pressed_keys.discard(key)


pyglet.app.run()