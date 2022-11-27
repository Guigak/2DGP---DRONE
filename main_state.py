# import
from pico2d import *
import random
import game_framework
import game_world
import server

# import class
from map import Map
from main_ui import Main_Ui

from drone import Drone
from enemy import Enemy
from item import Item
from electric_boom import Electric_Boom
from shuriken import Shuriken
from big_drone import Big_Drone
from mini_drone import Mini_Drone
# from electric_ball import Electric_Ball

# useful variable (maybe?)

# function

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN :
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            else :
                server.main_ui.handle_event(event)

# 게임 초기화 : 객체들을 생성

# data

def enter() :
    server.HEIGHT = get_canvas_height()
    server.WIDTH = get_canvas_width()

    server.map = Map()
    game_world.add_object(server.map, 0)

    server.main_ui = Main_Ui()
    game_world.add_object(server.main_ui, 1)


# 게임 종료 - 객체를 소멸
def exit() :
    server.map = None
    server.main_ui = None
    game_world.clear()

def update() :
    for game_object in game_world.all_objects():
        game_object.update()
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
    