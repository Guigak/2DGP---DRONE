from pico2d import *
import game_world
import server

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
            server.electric_booms.remove(self)
            game_world.remove_object(self)
        pass

    def draw(self):
        self.image.clip_draw(self.radius * 2 * self.frame_x, self.radius * 2 * (4 - self.frame_y),\
                            self.radius * 2, self.radius * 2,\
                            self.position_x, self.position_y)
        pass

    def handle_collision(self, other, group) :
        if group == 'enemy:eboom' :
            other.alive = False

    def Chk_with_Enemy(self, enemy) :
        tum_x = enemy.position_x - self.position_x
        tum_y = enemy.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + enemy.radius :
            enemy.alive = False
        pass