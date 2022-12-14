from pico2d import *
import game_world
import server

class Mini_Drone :
    image = None
    sound = None

    def __init__(self, drone_x, drone_y,drone_direct):
        if Mini_Drone.image == None :
            Mini_Drone.image = load_image('./resource/mini_drone.png')
        if Mini_Drone.sound == None :
            Mini_Drone.sound = load_wav('./resource/drone_sound.wav')
            Mini_Drone.sound.set_volume(32)

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
        self.frame_x = (self.frame_x + 1) % 2
        
        self.position_x = self.default_x + self.speed * self.time * math.cos(self.rad)
        self.position_y = self.default_y + self.speed * self.time * math.sin(self.rad)

        self.time += 1

        if (self.position_x < -self.radius) or (self.position_x > server.WIDTH + self.radius) :
            server.mini_drones.remove(self)
            game_world.remove_object(self)
        elif (self.position_y < -self.radius) or (self.position_y > server.HEIGHT + self.radius) :
            server.mini_drones.remove(self)
            game_world.remove_object(self)
        pass

    def draw(self):
        self.image.clip_composite_draw(self.radius * 2 * self.frame_x, self.frame_y,\
                                        self.radius * 2, self.radius * 2,\
                                        self.rad - 90 * math.pi / 180, 'n',\
                                        self.position_x, self.position_y,\
                                        self.radius * 2, self.radius * 2)
        pass

    def handle_collision(self, other, group) :
        if group == 'enemy:mdrone' :
            other.alive = False

    def play_sound(self) :
        self.sound.play()

    def Chk_with_Enemy(self, enemy) :
        tum_x = enemy.position_x - self.position_x
        tum_y = enemy.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + enemy.radius :
            enemy.alive = False
        pass