from pico2d import *
import game_framework

WIDTH, HEIGHT = 700, 900

class Map:
    def __init__(self):
        self.image = load_image('map.png')
        self.speed = 10
        self.move_y = 0

    def draw(self):
        self.image.draw(WIDTH // 2, HEIGHT // 2 - self.move_y)
        self.image.draw(WIDTH // 2, HEIGHT // 2 + HEIGHT - self.move_y)

        self.move_y = (self.move_y + self.speed) % HEIGHT

        print(self.move_y)

        # if self.move_y + self.speed < 900 :
        #     self.move_y += self.speed
        # else :
        #     self.move_y = 0

class Drone:
    def __init__(self):
        self.image = load_image('drone.png')
        self.radius = 50
        self.position_x = WIDTH // 2
        self.position_y = self.radius

        self.speed = 10

        self.up = False
        self.down = False
        self.left = False
        self.right = False
        
        self.shield = False
        self.shield_time = 0

        self.alive = True

        self.frame_x = 0
        self.frame_y = 0

    def update(self):
        if self.up :
            if self.position_y < HEIGHT - self.radius :
                self.position_y + self.speed

        if self.down :
            if self.position_y > self.radius :
                self.position_y - self.speed
                
        if self.left :
            if self.position_x > self.radius :
                self.position_x - self.speed
                
        if self.right :
            if self.position_x < WIDTH - self.radius :
                self.position_x + self.speed

    def draw(self):
        self.image.clip_draw(self.radius * 2 * self.frame_x, self.radius * 2 * (3 - self.frame_y),\
                            self.radius * 2, self.radius * 2,\
                            self.position_x, self.position_y)

        self.frame_x = (self.frame_x + 1) % 2
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
        elif event.type == SDL_KEYUP :
            if event.key == SDLK_UP :
                drone.up = False
            if event.key == SDLK_DOWN :
                drone.down = False
            if event.key == SDLK_LEFT :
                drone.left = False
            if event.key == SDLK_RIGHT :
                drone.right = False


# 게임 초기화 : 객체들을 생성

map = None
drone = None
running = True

def enter() :
    global map, drone, running

    map = Map()
    drone = Drone()
    running = True

# 게임 종료 - 객체를 소멸
def exit() :
    global map, drone

    del map
    del drone

def update() :
    pass    

def draw_world() :
    pass

def draw() :
    clear_canvas()
    map.draw()
    drone.update()
    drone.draw()
    update_canvas()

    delay(0.1)

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
    