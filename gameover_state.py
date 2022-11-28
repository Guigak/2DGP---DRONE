# import
from pico2d import *
import game_framework
import game_world
import server

# import class
from gameover_ui import Gameover_Ui

# useful variable (maybe?)

# function

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN :
            server.pause.handle_event(event)

# 게임 초기화 : 객체들을 생성

# data

def enter() :
    server.pause = Gameover_Ui()
    game_world.add_object(server.pause, 10)


# 게임 종료 - 객체를 소멸
def exit() :
    game_world.remove_object(server.pause)
    server.pause = None

def update() :
    server.pause.update()
    pass    

def draw_world() :
    pass

def draw() :    
    clear_canvas()
    for game_object in game_world.all_objects():
        game_object.draw()
    update_canvas()

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
    