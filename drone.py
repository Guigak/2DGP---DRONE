from pico2d import *
import server

class Drone :
    image = None
    shield_image = None

    def __init__(self):
        if Drone.image == None :
            Drone.image = load_image('drone.png')

        self.radius_default = self.radius = 50
        self.position_x = server.WIDTH // 2
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
        self.frame_x = (self.frame_x + 1) % 2
        
        # about moving
    
        if self.up :
            if self.position_y < server.HEIGHT - self.radius :
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
            if self.position_x < server.WIDTH - self.radius :
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

        # shield
        
        if self.shield :
            self.shield_image.clip_draw(self.shield_radius * 2 * self.shield_frame_x, self.shield_frame_y,\
                                self.shield_radius * 2, self.shield_radius * 2,\
                                self.position_x, self.position_y)

            self.shield_frame_x = (self.shield_frame_x + 1) % 4

        pass

    def handle_collision(self, other, group) :
        if group == 'drone:enemy' :
            if not self.shield :
                print('drone dead')
                self.alive = False
        elif group == 'drone:item' :
            if other.item_num == 2 :
                self.Shield_on()


    def Shield_on(self) :
        self.shield = True
        self.radius = self.shield_radius
        self.shield_time = 50
        self.shield_frame_x = 0

    def reset_flag(self) :
        self.up = False
        self.down = False
        self.left = False
        self.right = False

    def draw_gameover(self) :   # todo
        sx = 350
        sy = 650

        if self.position_x < 150 :
            sx -= 150 - self.position_x

        if self.position_x > 550 :
            sx += self.position_x - 550
        
        self.image.clip_draw(self.radius_default * 2 * self.frame_x, self.radius_default * 2 * (3 - self.frame_y),\
                            self.radius_default * 2, self.radius_default * 2,\
                            sx, sy)