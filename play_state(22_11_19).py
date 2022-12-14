from pico2d import *
import random
import game_framework

# useful variable (maybe?)

WIDTH, HEIGHT = 700, 900

# class

class Map :
    image = None

    def __init__(self):
        if Map.image == None :
            Map.image = load_image('map.png')
        self.speed = 10
        self.move_y = 0

    def draw(self):
        self.image.draw(WIDTH // 2, HEIGHT // 2 - self.move_y)
        self.image.draw(WIDTH // 2, HEIGHT // 2 + HEIGHT - self.move_y)

        self.move_y = (self.move_y + self.speed) % HEIGHT

class Drone :
    image = None
    shield_image = None

    def __init__(self):
        if Drone.image == None :
            Drone.image = load_image('drone.png')

        self.radius_default = self.radius = 50
        self.position_x = WIDTH // 2
        self.position_y = self.radius

        self.speed = 10

        self.up = False
        self.down = False
        self.left = False
        self.right = False

        self.direct = 2
        
        self.shield = False
        self.shield_time = 0

        self.alive = True

        self.frame_x = 0
        self.frame_y = 0

        # shield
        
        if Drone.shield_image == None :
            Drone.shield_image = load_image('electric_shield.png')

        self.shield_radius = 75

        self.shield_frame_x = 0
        self.shield_frame_y = 0

    def update(self):
        # about moving
    
        if self.up :
            if self.position_y < HEIGHT - self.radius :
                self.position_y += self.speed

            self.frame_y = 0

            self.direct = 2

        if self.down :
            if self.position_y > self.radius :
                self.position_y -= self.speed
                
            self.frame_y = 0

            self.direct = -2
                
        if self.left :
            if self.position_x > self.radius :
                self.position_x -= self.speed
                
            self.frame_y = 1

            self.direct = 4
                
        if self.right :
            if self.position_x < WIDTH - self.radius :
                self.position_x += self.speed
                
            self.frame_y = 1

            self.direct = 0

        # about drawing

        if (self.up and self.left) :
            self.frame_y = 2

            self.direct = 3

        if (self.down and self.right) :
            self.frame_y = 2
            
            self.direct = -1

        if (self.up and self.right) :
            self.frame_y = 3
            
            self.direct = 1

        if (self.down and self.left) :
            self.frame_y = 3
            
            self.direct = -3

        if (self.left and self.right)\
            and (self.up) :
            self.frame_y = 0
            
            self.direct = 2

        if (self.left and self.right)\
            and (self.down) :
            self.frame_y = 0
            
            self.direct = -2

        if (self.up and self.down)\
            and (self.left) :
            self.frame_y = 1
            
            self.direct = 4

        if (self.up and self.down)\
            and (self.right) :
            self.frame_y = 1
            
            self.direct = 0

        # about shield

        if self.shield :
            self.shield_time -= 1

            if self.shield_time == 0 :
                self.shield = False
                self.radius = self.radius_default

    def draw(self):
        self.image.clip_draw(self.radius_default * 2 * self.frame_x, self.radius_default * 2 * (3 - self.frame_y),\
                            self.radius_default * 2, self.radius_default * 2,\
                            self.position_x, self.position_y)

        self.frame_x = (self.frame_x + 1) % 2

        # shield
        
        if self.shield :
            self.shield_image.clip_draw(self.shield_radius * 2 * self.shield_frame_x, self.shield_frame_y,\
                                self.shield_radius * 2, self.shield_radius * 2,\
                                self.position_x, self.position_y)

            self.shield_frame_x = (self.shield_frame_x + 1) % 4

        pass

    def Shield_on(self) :
        self.shield = True
        self.radius = self.shield_radius
        self.shield_time = 50
        self.shield_frame_x = 0

class Enemy :
    image = None
    radius = 50

    def __init__(self):
        if Enemy.image == None :
            Enemy.image = load_image('enemy.png')
        #self.radius = 50
        self.default_x = self.position_x = random.randint(0, WIDTH)
        self.default_y = self.position_y = HEIGHT + self.radius

        self.speed = random.randint(3, 5)
        self.time = 0

        self.rad = 0
        self.reverse = False

        self.alive = True

        self.frame_x = 0
        self.frame_y = 0

    def update(self):
        if self.reverse :
            self.position_x = self.default_x - self.speed * self.time * math.cos(self.rad)
            self.position_y = self.default_y - self.speed * self.time * math.sin(self.rad)
        else :
            self.position_x = self.default_x + self.speed * self.time * math.cos(self.rad)
            self.position_y = self.default_y + self.speed * self.time * math.sin(self.rad)

        self.time += 1

        if (self.position_x < -self.radius) or (self.position_x > WIDTH + self.radius) :
            self.alive = False

        if self.position_y < -self.radius :
            self.alive = False

        if not self.alive :
            self.default_x = random.randint(0, WIDTH)
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

        self.frame_x = (self.frame_x + 1) % 2

    def Cal_rad(self) :
        dx = drone.position_x - self.default_x
        dy = drone.position_y - self.default_y

        if dx < 0 :
            self.reverse = True

        if dx == 0 :
            self.rad = math.atan(dy / 1)
        else :
            self.rad = math.atan(dy / dx)

    def Chk_with_Drone(self) :
        tum_x = drone.position_x - self.position_x
        tum_y = drone.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + drone.radius :
            if drone.shield :
                self.alive = False
            else :
                drone.alive = False
        pass

class Item:
    image = None

    def __init__(self):
        if Item.image == None :
            Item.image = load_image('item_icons.png')
        self.radius = 25
        self.default_x = self.position_x = random.randint(0, WIDTH)
        self.default_y = self.position_y = HEIGHT + self.radius

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
                
        if self.position_x >= WIDTH - self.radius :
            self.default_x = WIDTH - self.radius
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
            if self.position_y >= HEIGHT - self.radius :
                self.default_y = HEIGHT - self.radius
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
        tum_x = drone.position_x - self.position_x
        tum_y = drone.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + drone.radius :
            self.alive = False

        if self.alive == False :
            match self.item_num :
                case 0 :
                    Add_Eboom(self.position_x, self.position_y)
                case 1 :
                    Add_Shuriken(self.position_x, self.position_y)
                    Add_Shuriken(self.position_x, self.position_y)
                    Add_Shuriken(self.position_x, self.position_y)
                case 2 :
                    drone.Shield_on()
                case 3 :
                    Add_Bdrone(self.position_x, self.position_y)
                case 4 :
                    Get_Mdrone()
                case 5 :
                    Add_Eball(self.position_x, self.position_y)
                case _:
                    pass
        
        return self.alive
        pass

class Electric_Boom:
    image = None

    def __init__(self, item_x, item_y):
        if Electric_Boom.image == None :
            Electric_Boom.image = load_image('electric_boom.png')
        self.radius = 100
        self.position_x = item_x
        self.position_y = item_y

        self.time = 0

        self.alive = True

        self.frame_x = 0
        self.frame_y = 0
        pass

    def update(self):
        self.time += 1

        self.frame_x = self.time % 5
        self.frame_y = self.time // 5

        if self.time == 25 :
            self.alive = False

        return self.alive
        pass

    def draw(self):
        self.image.clip_draw(self.radius * 2 * self.frame_x, self.radius * 2 * (4 - self.frame_y),\
                            self.radius * 2, self.radius * 2,\
                            self.position_x, self.position_y)
        pass

    def Chk_with_Enemy(self, enemy) :
        tum_x = enemy.position_x - self.position_x
        tum_y = enemy.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + enemy.radius :
            enemy.alive = False
        pass

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

        self.target = enemies[random.randint(0, len(enemies) - 1)]

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
                        self.alive = False
                    else :
                        self.frame_y = self.frame_y % 3
                        self.explosion_loop += 1

        return self.alive
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

    def targeting(self) :
        self.target = enemies[random.randint(0, len(enemies) - 1)]

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

        # if tum < self.radius + enemy.radius :
        #     if self.explosion :
        #         enemy.alive = False
        #     else :
        #         if self.target == enemy :
        #             if tum < self.radius :
        #                 self.explosion = True

        #                 self.radius = 75
        #                 self.frame_x = -1
        #                 self.frame_y = 0
        #         else :
        #             enemy.alive = False
        pass

class Big_Drone :
    image = None

    def __init__(self, item_x, item_y):
        if Big_Drone.image == None :
            Big_Drone.image = load_image('big_drone.png')

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
        self.position_y = self.position_y + self.speed

        self.rect['y1'] = self.rect['y1'] + self.speed
        self.rect['y2'] = self.rect['y2'] + self.speed

        if self.rect['y2'] > HEIGHT :
            self.alive = False

        return self.alive
        pass

    def draw(self):
        self.image.clip_draw(self.width * self.frame_x, self.frame_y,\
                            self.width, self.height,\
                            self.position_x, self.position_y)

        self.frame_x = (self.frame_x + 1) % 2
        pass

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

class Mini_Drone :
    image = None

    def __init__(self, drone_x, drone_y,drone_direct):
        if Mini_Drone.image == None :
            Mini_Drone.image = load_image('mini_drone.png')

        self.default_x = self.position_x = drone_x
        self.default_y = self.position_y = drone_y

        self.radius = 25

        self.rad = 45 * drone_direct * math.pi / 180

        self.speed = 5

        self.time = 0

        self.alive = True

        self.frame_x = 0
        self.frame_y = 0
        pass

    def update(self):
        self.position_x = self.default_x + self.speed * self.time * math.cos(self.rad)
        self.position_y = self.default_y + self.speed * self.time * math.sin(self.rad)

        self.time += 1

        if (self.position_x < -self.radius) or (self.position_x > WIDTH + self.radius) :
            self.alive = False

        if (self.position_y < -self.radius) or (self.position_y > HEIGHT + self.radius) :
            self.alive = False

        return self.alive
        pass

    def draw(self):
        self.image.clip_composite_draw(self.radius * 2 * self.frame_x, self.frame_y,\
                                        self.radius * 2, self.radius * 2,\
                                        self.rad - 90 * math.pi / 180, 'n',\
                                        self.position_x, self.position_y,\
                                        self.radius * 2, self.radius * 2)

        self.frame_x = (self.frame_x + 1) % 2
        pass

    def Chk_with_Enemy(self, enemy) :
        tum_x = enemy.position_x - self.position_x
        tum_y = enemy.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + enemy.radius :
            enemy.alive = False
        pass

class Electric_Ball :
    image = None

    def __init__(self, item_x, item_y, drone_direct):
        if Electric_Ball.image == None :
            Electric_Ball.image = load_image('electric_ball.png')

        self.radius = 75
        self.default_x = self.position_x = item_x
        self.default_y = self.position_y = item_y
        
        self.rad = 45 * drone_direct * math.pi / 180

        self.speed = 10
        self.time = 0

        self.time_alive = 0
        self.alive = True

        self.frame_x = 0
        self.frame_y = 0        
        pass

    def update(self):
        self.time += 1
        self.time_alive += 1
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
                
        if self.position_x >= WIDTH - self.radius :
            self.default_x = WIDTH - self.radius
            self.default_y = self.position_y

            if self.rad < 0 :
                self.rad = self.rad - 2 * (math.pi / 2 + self.rad)
            else :
                self.rad = self.rad + 2 * (math.pi / 2 - self.rad)

            self.time = 0
                
        if self.position_y <= self.radius :
            self.default_y = self.radius
            self.default_x = self.position_x

            self.rad = -self.rad

            self.time = 0

        if self.position_y >= HEIGHT - self.radius :
            self.default_y = HEIGHT - self.radius
            self.default_x = self.position_x

            self.rad = -self.rad

            self.time = 0

        if self.time_alive == 100 :
            self.alive = False

        return self.alive
        pass

    def draw(self):
        self.image.clip_draw(self.radius * 2 * self.frame_x, self.frame_y,\
                            self.radius * 2, self.radius * 2,\
                            self.position_x, self.position_y)

        self.frame_x = (self.frame_x + 1) % 4
        pass

    def Chk_with_Enemy(self, enemy) :
        tum_x = enemy.position_x - self.position_x
        tum_y = enemy.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + enemy.radius :
            enemy.alive = False
        pass


# function

def Get_Mdrone() :
    global num_create_mdrone

    num_create_mdrone += 10

def Add_Enemy() :
    global enemies, time_create_enemy

    if len(enemies) < 50 :
        if time_create_enemy == len(enemies) :
            enemies += [Enemy()]
            enemies[len(enemies) - 1].Cal_rad()

            time_create_enemy = 0
        else :
            time_create_enemy += 1

    pass

def Add_Item() :
    global items, time_create_item

    if len(items) < 3 :
        if time_create_item == 0 :
            items += [Item()]

            time_create_item = 100

    if time_create_item != 0 :
        time_create_item -= 1
    pass

def Add_Eboom(x, y) :
    global electric_booms

    electric_booms += [Electric_Boom(x, y)]
    pass

def Add_Bdrone(x, y) :
    global big_drones

    big_drones += [Big_Drone(x, y)]
    pass

def Add_Mdrone() :
    global mini_drones, time_create_mdrone, num_create_mdrone

    if num_create_mdrone != 0 :
        if time_create_mdrone == 0 :
            mini_drones += [Mini_Drone(drone.position_x, drone.position_y, drone.direct)]

            num_create_mdrone -= 1
            time_create_mdrone = 4

    if time_create_mdrone != 0 :
        time_create_mdrone -= 1
    pass

def Add_Eball(x, y) :
    global electric_balls

    electric_balls += [Electric_Ball(x, y, drone.direct)]
    pass

def Add_Shuriken(x, y) :
    global shurikens

    shurikens += [Shuriken(x, y)]
    pass

def Chk_Drone_N_Enemy() :
    for enemy in enemies :
        enemy.Chk_with_Drone()
    pass

def Chk_Drone_N_Item() :
    if len(items) != 0 :
        for item in items :
            if item.Chk_with_Drone() == False :
                items.remove(item)
    pass

def Chk_Eboom_N_Enemy() :
    for eboom in electric_booms :
        for enemy in enemies :
            eboom.Chk_with_Enemy(enemy)
    pass

def Chk_Bdrone_N_Enemy() :
    for bdrone in big_drones :
        for enemy in enemies :
            bdrone.Chk_with_Enemy(enemy)
    pass

def Chk_Mdrone_N_Enemy() :
    for mdrone in mini_drones :
        for enemy in enemies :
            mdrone.Chk_with_Enemy(enemy)
    pass

def Chk_Eball_N_Enemy() :
    for eball in electric_balls :
        for enemy in enemies :
            eball.Chk_with_Enemy(enemy)
    pass

def Chk_Shuriken_N_Enemy() :
    for shuriken in shurikens :
        for enemy in enemies :
            shuriken.Chk_with_Enemy(enemy)

def Chk_Game_End() :
    if not drone.alive :
        #game_framework.quit()   # ??????
        pass
    pass

def handle_events():
    global running

    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN :
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_UP :
                drone.up = True
            if event.key == SDLK_DOWN :
                drone.down = True
            if event.key == SDLK_LEFT :
                drone.left = True
            if event.key == SDLK_RIGHT :
                drone.right = True
            # test
            if event.key == SDLK_1 :
                Add_Eboom(drone.position_x, drone.position_y)
            if event.key == SDLK_2 :
                Add_Shuriken(drone.position_x, drone.position_y)
                Add_Shuriken(drone.position_x, drone.position_y)
                Add_Shuriken(drone.position_x, drone.position_y)
            if event.key == SDLK_3 :
                drone.Shield_on()
            if event.key == SDLK_4 :
                Add_Bdrone(drone.position_x, drone.position_y)
            if event.key == SDLK_5 :
                Get_Mdrone()
            if event.key == SDLK_6 :
                Add_Eball(drone.position_x, drone.position_y)
            
        elif event.type == SDL_KEYUP :
            if event.key == SDLK_UP :
                drone.up = False
            if event.key == SDLK_DOWN :
                drone.down = False
            if event.key == SDLK_LEFT :
                drone.left = False
            if event.key == SDLK_RIGHT :
                drone.right = False


# ?????? ????????? : ???????????? ??????

# data

map = None
drone = None
enemies = [None]
items = [None]
electric_booms = [None]
big_drones = [None]
mini_drones = [None]
electric_balls = [None]
shurikens = [None]

time_create_enemy = None
time_create_item = None
time_create_mdrone = None

num_create_mdrone = None

running = True

def enter() :
    global map, drone, enemies, time_create_enemy, items, time_create_item, electric_booms, big_drones, mini_drones, time_create_mdrone, num_create_mdrone, electric_balls, shurikens, running

    map = Map()
    drone = Drone()
    enemies = [Enemy()]
    items = [Item()]
    electric_booms = []
    big_drones = []
    mini_drones = []
    electric_balls = []
    shurikens = []

    enemies[0].Cal_rad()

    time_create_enemy = 0
    time_create_item = 100
    time_create_mdrone = 0

    num_create_mdrone = 0
    running = True

# ?????? ?????? - ????????? ??????
def exit() :
    global map, drone, enemies, items, electric_booms, big_drones, mini_drones, electric_balls, shurikens

    del map
    del drone
    del enemies
    del items
    del electric_booms
    del big_drones
    del mini_drones
    del electric_balls
    del shurikens

def update() :
    drone.update()
    for enemy in enemies :
        enemy.update()

    for item in items :
        item.update()

    for eboom in electric_booms :
        if eboom.update() == False :
            electric_booms.remove(eboom)

    for bdrone in big_drones :
        if bdrone.update() == False :
            big_drones.remove(bdrone)

    for mdrone in mini_drones :
        if mdrone.update() == False :
            mini_drones.remove(mdrone)

    for eball in electric_balls :
        if eball.update() == False :
            electric_balls.remove(eball)

    for shuriken in shurikens :
        if shuriken.update() == False :
            shurikens.remove(shuriken)

    Add_Enemy()
    Add_Item()
    Add_Mdrone()
    Chk_Drone_N_Enemy()
    Chk_Drone_N_Item()
    Chk_Eboom_N_Enemy()
    Chk_Bdrone_N_Enemy()
    Chk_Mdrone_N_Enemy()
    Chk_Eball_N_Enemy()
    Chk_Shuriken_N_Enemy()
    Chk_Game_End()
    pass    

def draw_world() :
    pass

def draw() :
    clear_canvas()
    map.draw()
    drone.draw()

    for enemy in enemies :
        enemy.draw()

    for item in items :
        item.draw()
        
    for eboom in electric_booms :
        eboom.draw()

    for bdrone in big_drones :
        bdrone.draw()

    for mdrone in mini_drones :
        mdrone.draw()

    for eball in electric_balls :
        eball.draw()

    for shuriken in shurikens :
        shuriken.draw()
        
    update_canvas()

    delay(0.05)

def pause():
    pass

def resume():
    pass

def test_self() :
    import sys
    this_module = sys.modules['__main__']
    pico2d.open_canvas(700, 900)
    game_framework.run(this_module)
    pico2d.close_canvas

if __name__ == '__main__' :
    test_self()
    