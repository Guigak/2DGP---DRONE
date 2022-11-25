from pico2d import *
import server

import random

class Item:
    image = None

    def __init__(self):
        if Item.image == None :
            Item.image = load_image('item_icons.png')
        self.radius = 25
        self.default_x = self.position_x = random.randint(0, server.WIDTH)
        self.default_y = self.position_y = server.HEIGHT + self.radius

        self.rand_num = random.randint(0, 24)

        self.speed = 5 + self.rand_num % 3
        self.time = 0

        self.direct = self.rand_num % 2 # 0 : left, 1 : right

        if self.direct == 0 :
            self.rad = -1 * random.uniform(15 * math.pi / 180, 60 * math.pi / 180)
        else :
            self.rad = -1 * random.uniform(105 * math.pi / 180, 165 * math.pi / 180)

        self.bounce = False

        self.alive = True

        # self.item_num = 1
        self.item_num = self.rand_num % 6
        # 0 : E_Boom, 1 : Shuriken, 2 : E_Shield, 3 : Big, 4 : Mini, 5 : E_Ball

        self.frame_x = self.item_num
        self.frame_y = 0

        pass

    def update(self):
        self.time += 1
        self.position_x = self.default_x + self.speed * self.time * math.cos(self.rad)
        self.position_y = self.default_y + self.speed * self.time * math.sin(self.rad)

        if self.position_x <= self.radius :
            self.default_x = self.radius
            self.default_y = self.position_y

            if self.rad < 0 :
                self.rad = self.rad - 2 * (math.pi / 2 + self.rad)
            else :
                self.rad = self.rad + 2 * (math.pi / 2 - self.rad)

            self.time = 0
            self.bounce = True
                
        if self.position_x >= server.WIDTH - self.radius :
            self.default_x = server.WIDTH - self.radius
            self.default_y = self.position_y

            if self.rad < 0 :
                self.rad = self.rad - 2 * (math.pi / 2 + self.rad)
            else :
                self.rad = self.rad + 2 * (math.pi / 2 - self.rad)

            self.time = 0
            self.bounce = True
                
        if self.position_y <= self.radius :
            self.default_y = self.radius
            self.default_x = self.position_x

            self.rad = -self.rad

            self.time = 0
            self.bounce = True
                    
        if self.bounce :
            if self.position_y >= server.HEIGHT - self.radius :
                self.default_y = server.HEIGHT - self.radius
                self.default_x = self.position_x

                self.rad = -self.rad

                self.time = 0
                self.bounce = True

        pass

    def draw(self):
        self.image.clip_draw(self.radius * 2 * self.frame_x, self.frame_y,\
                            self.radius * 2, self.radius * 2,\
                            self.position_x, self.position_y)
        pass

    def Chk_with_Drone(self) :
        tum_x = server.drone.position_x - self.position_x
        tum_y = server.drone.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + server.drone.radius :
            self.alive = False

        if self.alive == False :
            match self.item_num :
                # case 0 :
                #     Add_Eboom(self.position_x, self.position_y)
                # case 1 :
                #     Add_Shuriken(self.position_x, self.position_y)
                #     Add_Shuriken(self.position_x, self.position_y)
                #     Add_Shuriken(self.position_x, self.position_y)
                # case 2 :
                #     drone.Shield_on()
                # case 3 :
                #     Add_Bdrone(self.position_x, self.position_y)
                # case 4 :
                #     Get_Mdrone()
                # case 5 :
                #     Add_Eball(self.position_x, self.position_y)
                case _:
                    pass
        
        return self.alive
        pass