from pico2d import *
import server

class Drone :
    image = None
    shield_image = None
    shield_sound = None

    def __init__(self):
        if Drone.image == None :
            Drone.image = load_image('./resource/drone.png')
        if Drone.shield_sound == None :
            Drone.shield_sound = load_music('./resource/shield_sound.wav')
            Drone.shield_sound.set_volume(32)

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

        self.sx = 0
        self.sy = 0

        # shield
        
        if Drone.shield_image == None :
            Drone.shield_image = load_image('./resource/electric_shield.png')

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
        
        if self.shield and\
            (self.shield_time > 25 or self.shield_time % 2 == 1) :
            self.shield_image.clip_draw(self.shield_radius * 2 * self.shield_frame_x, self.shield_frame_y,\
                                self.shield_radius * 2, self.shield_radius * 2,\
                                self.position_x, self.position_y)

            self.shield_frame_x = (self.shield_frame_x + 1) % 4

        pass

    def handle_collision(self, other, group) :
        if group == 'drone:enemy' :
            if not self.shield :
                if self.Chk_collision(other) :
                    self.alive = False
        elif group == 'drone:item' :
            if other.item_num == 2 :
                self.Shield_on()


    def Shield_on(self) :
        self.shield_sound.play()

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
        self.sx = 350
        self.sy = 650

        if self.position_x < 200 :
            self.sx -= 200 - self.position_x
        elif self.position_x > 500 :
            self.sx += self.position_x - 500
        
        self.image.clip_draw(self.radius_default * 2 * self.frame_x, self.radius_default * 2 * (3 - self.frame_y),\
                            self.radius_default * 2, self.radius_default * 2,\
                            self.sx, self.sy)

    def Chk_collision(self, other) :
        tum_x = self.position_x - other.position_x
        tum_y = self.position_y - other.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + other.radius - 5 :
            return True
        
        return False