from pico2d import *
import game_framework

class Map:
    def __init__(self):
        self.image = load_image('map.png')
        self.speed = 10
        self.move_y = 0

    def draw(self):
        self.image.draw(350, 450 - self.move_y)
        self.image.draw(350, 450 + 900 - self.move_y)

        self.move_y = (self.move_y + self.speed) % 900

        print(self.move_y)

        # if self.move_y + self.speed < 900 :
        #     self.move_y += self.speed
        # else :
        #     self.move_y = 0

class Drone:
    def __init__(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

def handle_events():
    global running
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN :
            if event.key == SDLK_ESCAPE:
                pass


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
    