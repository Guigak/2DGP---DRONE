from pico2d import *
import server

import random

class Enemy :
    image = None
    radius = 50

    def __init__(self):
        if Enemy.image == None :
            Enemy.image = load_image('./resource/enemy.png')
        #self.radius = 50
        self.default_x = self.position_x = random.randint(0, server.WIDTH)
        self.default_y = self.position_y = server.HEIGHT + self.radius

        self.speed = random.randint(3, 5)
        self.time = 0

        self.rad = 0
        self.reverse = False

        self.alive = True

        self.frame_x = 0
        self.frame_y = 0

        self.Cal_rad()

    def update(self):
        self.frame_x = (self.frame_x + 1) % 2
        
        if self.reverse :
            self.position_x = self.default_x - self.speed * self.time * math.cos(self.rad)
            self.position_y = self.default_y - self.speed * self.time * math.sin(self.rad)
        else :
            self.position_x = self.default_x + self.speed * self.time * math.cos(self.rad)
            self.position_y = self.default_y + self.speed * self.time * math.sin(self.rad)

        self.time += 1

        if (self.position_x < -self.radius) or (self.position_x > server.WIDTH + self.radius) :
            self.alive = False

        if self.position_y < -self.radius :
            self.alive = False

        #
        if not self.alive :
            self.default_x = random.randint(0, server.WIDTH)
            self.position_x = self.default_x
            self.position_y = self.default_y
            self.reverse = False
            self.Cal_rad()
            self.time = 0

            self.alive = True

    def draw(self):
        self.image.clip_composite_draw(self.radius * 2 * self.frame_x, self.frame_y,\
                                        self.radius * 2, self.radius * 2,\
                                        self.rad, 'n',\
                                        self.position_x, self.position_y,\
                                        self.radius * 2, self.radius * 2)

    def handle_collision(self, other, group) :
        if group == 'drone:enemy' :
            if other.shield :
                self.alive = False
                server.score.add_score()
        else :
            server.score.add_score()

    def Cal_rad(self) :
        dx = server.drone.position_x - self.default_x
        dy = server.drone.position_y - self.default_y

        if dx < 0 :
            self.reverse = True

        if dx == 0 :
            self.rad = math.atan(dy / 1)
        else :
            self.rad = math.atan(dy / dx)

    def draw_gameover(self) :
        sxm = server.drone.position_x   # screen x middle
        sym = server.drone.position_y

        if sxm < 200 :
            sxm = 200
        elif sxm > 500 :
            sxm = 500

        if sxm - 200 < self.position_x < sxm + 200\
            and sym - 150 < self.position_y < sym + 150 :
            sx = 350 + (self.position_x - sxm)
            sy = 650 + (self.position_y - sym)

            self.image.clip_composite_draw(self.radius * 2 * self.frame_x, self.frame_y,\
                                        self.radius * 2, self.radius * 2,\
                                        self.rad, 'n',\
                                        sx, sy,\
                                        self.radius * 2, self.radius * 2)
        
        
        

    def Chk_with_Drone(self) :
        tum_x = server.drone.position_x - self.position_x
        tum_y = server.drone.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + server.drone.radius :
            if server.drone.shield :
                self.alive = False
            else :
                server.drone.alive = False
        pass