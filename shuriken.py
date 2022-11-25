from pico2d import *
import game_world
import server

import random

class Shuriken :
    image_d = None
    image_e = None

    def __init__(self, item_x, item_y):
        if Shuriken.image_d == None :
            Shuriken.image_d = load_image('shuriken_drone.png')
            Shuriken.image_e = load_image('shuriken_explosion.png')

        self.radius = 50    # e : 75
        self.position_x = item_x
        self.position_y = item_y

        self.move_x = random.randint(-5, 5)
        self.move_y = random.randint(-5, 5)

        self.max_speed = 10

        self.target = server.enemies[random.randint(0, len(server.enemies) - 1)]

        self.explosion = False
        self.explosion_loop = 0

        self.alive = True

        self.frame_x = 0
        self.frame_y = 0
        pass

    def update(self):
        if self.explosion == False :
            position_tx = self.target.position_x
            position_ty = self.target.position_y

            if self.position_x < position_tx :
                if self.move_x < self.max_speed :
                    self.move_x += 1
            elif self.position_x > position_tx :
                if self.move_x > -self.max_speed :
                    self.move_x -= 1

            if self.position_y < position_ty :
                if self.move_y < self.max_speed :
                    self.move_y += 1
            elif self.position_y > position_ty :
                if self.move_y > -self.max_speed :
                    self.move_y -= 1

            self.position_x += self.move_x
            self.position_y += self.move_y

            self.frame_x += 1

            if self.frame_x >= 4 :
                self.frame_x = self.frame_x % 4

                self.frame_y += 1
                self.frame_y = self.frame_y % 3
        else :
            self.frame_x += 1

            if self.frame_x >= 2 :
                self.frame_x = self.frame_x % 2

                self.frame_y += 1
                
                if self.frame_y >= 3 :
                    if self.explosion_loop == 3 :
                        game_world.remove_object(self)
                    else :
                        self.frame_y = self.frame_y % 3
                        self.explosion_loop += 1
        pass

    def draw(self):
        if self.explosion == False :
            self.image_d.clip_draw(self.radius * 2 * self.frame_x, self.radius * 2 * (2 - self.frame_y),\
                                self.radius * 2, self.radius * 2,\
                                self.position_x, self.position_y)
        else :
            self.image_e.clip_draw(self.radius * 2 * self.frame_x, self.radius * 2 * (2 - self.frame_y),\
                                self.radius * 2, self.radius * 2,\
                                self.position_x, self.position_y)
        pass

    def handle_collision(self, other, group) :
        if group == 'enemy:shuriken' :
            other.alive = False

            if self.explosion == False :
                if self.target == other :
                    self.explosion = True

                    self.radius = 75
                    self.frame_x = -1
                    self.frame_y = 0

    def targeting(self) :
        self.target = server.enemies[random.randint(0, len(server.enemies) - 1)]

    def Chk_with_Enemy(self, enemy) :
        tum_x = enemy.position_x - self.position_x
        tum_y = enemy.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + enemy.radius :
            enemy.alive = False

            if self.explosion == False :
                if self.target == enemy :
                    self.explosion = True

                    self.radius = 75
                    self.frame_x = -1
                    self.frame_y = 0
        pass