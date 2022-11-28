from pico2d import *
import server

class Map :
    image = None

    def __init__(self):
        if Map.image == None :
            Map.image = load_image('map_r.png')
        self.speed = 10
        self.move_y = 0

    def update(self) :
        self.move_y = (self.move_y + self.speed) % server.HEIGHT

    def draw(self):
        self.image.draw(server.WIDTH // 2, server.HEIGHT // 2 - self.move_y)
        self.image.draw(server.WIDTH // 2, server.HEIGHT // 2 + server.HEIGHT - self.move_y)

    def draw_gameover(self) :   # todo
        sx = server.drone.position_x - 200
        sy = server.drone.position_y - 150 - self.move_y

        self.image.clip_draw_to_origin(server.drone.position_x - 200, server.drone.position_y - 150 - self.move_y,\
                                        400, 300,\
                                        150, 500)