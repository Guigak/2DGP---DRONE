from pico2d import *
import game_world
import server

from enemy import Enemy

class Big_Drone :
    image = None
    sound = None

    def __init__(self, item_x, item_y):
        if Big_Drone.image == None :
            Big_Drone.image = load_image('./resource/big_drone.png')
        if Big_Drone.sound == None :
            Big_Drone.sound = load_music('./resource/drone_sound.wav')
            Big_Drone.sound.set_volume(32)

        self.sound.play()

        self.width = Big_Drone.image.w // 2
        self.height = Big_Drone.image.h

        self.position_x = item_x
        self.position_y = item_y

        self.rect = {'x1' : self.position_x - self.width / 2 - Enemy.radius, 'y1' : self.position_y + self.height / 2 + Enemy.radius,\
                    'x2' : self.position_x + self.width / 2 + Enemy.radius, 'y2' : self.position_y - self.height / 2 - Enemy.radius}

        self.speed = 8

        self.alive = True

        self.frame_x = 0
        self.frame_y = 0
        pass

    def update(self):
        self.frame_x = (self.frame_x + 1) % 2
        
        self.position_y = self.position_y + self.speed

        self.rect['y1'] = self.rect['y1'] + self.speed
        self.rect['y2'] = self.rect['y2'] + self.speed

        if self.rect['y2'] > server.HEIGHT :
            server.big_drones.remove(self)
            game_world.remove_object(self)
        pass

    def draw(self):
        self.image.clip_draw(self.width * self.frame_x, self.frame_y,\
                            self.width, self.height,\
                            self.position_x, self.position_y)
        pass

    def handle_collision(self, other, group) :
        if group == 'enemy:bdrone' :
            other.alive = False

    def Chk_with_Enemy(self, enemy) :
        chk1 = chk2 = False

        if enemy.position_x >= self.rect['x1']\
            and enemy.position_x <= self.rect['x2'] :
            chk1 = True

        if enemy.position_y <= self.rect['y1']\
            and enemy.position_y >= self.rect['y2'] :
            chk2 = True

        if chk1 and chk2 :
            enemy.alive = False
        pass