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
        y_is_out = False

        sx = server.drone.position_x - 200
        sy = server.drone.position_y - 150 + self.move_y

        dx = 400
        dy = 300

        sx = clamp(0, sx, server.WIDTH - 400)
        
        if sy > server.HEIGHT :
            sy -= server.HEIGHT

        if sy + 150 > server.HEIGHT :
            y_is_out = True
            dy = server.HEIGHT - (sy - 300)

        if sy < 0 :
            y_is_out = True
            sy += server.HEIGHT
            dy = server.HEIGHT - (sy - 300)


        self.image.clip_draw_to_origin(sx, sy, dx, dy, 150, 500)

        if y_is_out :
            self.image.clip_draw_to_origin(sx, 0, 400, 300 - dy, 150, 500 + dy)