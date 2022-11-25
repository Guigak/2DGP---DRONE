from pico2d import *
import game_world
import server

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
                
        if self.position_x >= server.WIDTH - self.radius :
            self.default_x = server.WIDTH - self.radius
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

        if self.position_y >= server.HEIGHT - self.radius :
            self.default_y = server.HEIGHT - self.radius
            self.default_x = self.position_x

            self.rad = -self.rad

            self.time = 0

        if self.time_alive == 100 :
            server.electric_balls.remove(self)
            game_world.remove_object(self)
        pass

    def draw(self):
        self.image.clip_draw(self.radius * 2 * self.frame_x, self.frame_y,\
                            self.radius * 2, self.radius * 2,\
                            self.position_x, self.position_y)

        self.frame_x = (self.frame_x + 1) % 4
        pass

    def handle_collision(self, other, group) :
        if group == 'enemy:eball' :
            other.alive = False

    def Chk_with_Enemy(self, enemy) :
        tum_x = enemy.position_x - self.position_x
        tum_y = enemy.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + enemy.radius :
            enemy.alive = False
        pass