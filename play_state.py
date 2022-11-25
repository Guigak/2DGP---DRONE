# import
from pico2d import *
import random
import game_framework
import game_world
import server

# import class
from map import Map
from drone import Drone
# from enemy import Enemy
# from item import Item
# from electric_boom import Electric_Boom
# from shuriken import Shuriken
# from big_drone import Big_Drone
# from mini_drone import Mini_Drone
# from electric_ball import Electric_Ball

# useful variable (maybe?)

# function

# def Get_Mdrone() :
#     global num_create_mdrone

#     num_create_mdrone += 10

# def Add_Enemy() :
#     global enemies, time_create_enemy

#     if len(enemies) < 50 :
#         if time_create_enemy == len(enemies) :
#             enemies += [Enemy()]
#             enemies[len(enemies) - 1].Cal_rad()

#             time_create_enemy = 0
#         else :
#             time_create_enemy += 1

#     pass

# def Add_Item() :
#     global items, time_create_item

#     if len(items) < 3 :
#         if time_create_item == 0 :
#             items += [Item()]

#             time_create_item = 100

#     if time_create_item != 0 :
#         time_create_item -= 1
#     pass

# def Add_Eboom(x, y) :
#     global electric_booms

#     electric_booms += [Electric_Boom(x, y)]
#     pass

# def Add_Bdrone(x, y) :
#     global big_drones

#     big_drones += [Big_Drone(x, y)]
#     pass

# def Add_Mdrone() :
#     global mini_drones, time_create_mdrone, num_create_mdrone

#     if num_create_mdrone != 0 :
#         if time_create_mdrone == 0 :
#             mini_drones += [Mini_Drone(drone.position_x, drone.position_y, drone.direct)]

#             num_create_mdrone -= 1
#             time_create_mdrone = 4

#     if time_create_mdrone != 0 :
#         time_create_mdrone -= 1
#     pass

# def Add_Eball(x, y) :
#     global electric_balls

#     electric_balls += [Electric_Ball(x, y, drone.direct)]
#     pass

# def Add_Shuriken(x, y) :
#     global shurikens

#     shurikens += [Shuriken(x, y)]
#     pass

# def Chk_Drone_N_Enemy() :
#     for enemy in enemies :
#         enemy.Chk_with_Drone()
#     pass

# def Chk_Drone_N_Item() :
#     if len(items) != 0 :
#         for item in items :
#             if item.Chk_with_Drone() == False :
#                 items.remove(item)
#     pass

# def Chk_Eboom_N_Enemy() :
#     for eboom in electric_booms :
#         for enemy in enemies :
#             eboom.Chk_with_Enemy(enemy)
#     pass

# def Chk_Bdrone_N_Enemy() :
#     for bdrone in big_drones :
#         for enemy in enemies :
#             bdrone.Chk_with_Enemy(enemy)
#     pass

# def Chk_Mdrone_N_Enemy() :
#     for mdrone in mini_drones :
#         for enemy in enemies :
#             mdrone.Chk_with_Enemy(enemy)
#     pass

# def Chk_Eball_N_Enemy() :
#     for eball in electric_balls :
#         for enemy in enemies :
#             eball.Chk_with_Enemy(enemy)
#     pass

# def Chk_Shuriken_N_Enemy() :
#     for shuriken in shurikens :
#         for enemy in enemies :
#             shuriken.Chk_with_Enemy(enemy)

# def Chk_Game_End() :
#     if not drone.alive :
#         #game_framework.quit()   # 임시
#         pass
#     pass

def handle_events():
    events = get_events()

    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN :
            if event.key == SDLK_ESCAPE:
                game_framework.quit()
            if event.key == SDLK_UP :
                server.drone.up = True
            if event.key == SDLK_DOWN :
                server.drone.down = True
            if event.key == SDLK_LEFT :
                server.drone.left = True
            if event.key == SDLK_RIGHT :
                server.drone.right = True
            # test
            # if event.key == SDLK_1 :
            #     Add_Eboom(server.drone.position_x, server.drone.position_y)
            # if event.key == SDLK_2 :
            #     Add_Shuriken(server.drone.position_x, server.drone.position_y)
            #     Add_Shuriken(server.drone.position_x, server.drone.position_y)
            #     Add_Shuriken(server.drone.position_x, server.drone.position_y)
            # if event.key == SDLK_3 :
            #     server.drone.Shield_on()
            # if event.key == SDLK_4 :
            #     Add_Bserver.drone(server.drone.position_x, server.drone.position_y)
            # if event.key == SDLK_5 :
            #     Get_Mserver.drone()
            # if event.key == SDLK_6 :
            #     Add_Eball(server.drone.position_x, server.drone.position_y)
            
        elif event.type == SDL_KEYUP :
            if event.key == SDLK_UP :
                server.drone.up = False
            if event.key == SDLK_DOWN :
                server.drone.down = False
            if event.key == SDLK_LEFT :
                server.drone.left = False
            if event.key == SDLK_RIGHT :
                server.drone.right = False


# 게임 초기화 : 객체들을 생성

# data

def enter() :
    server.HEIGHT = get_canvas_height()
    server.WIDTH = get_canvas_width()
    
    server.map = Map()
    game_world.add_object(server.map, 0)

    server.drone = Drone()
    game_world.add_object(server.drone, 1)

    # enemies = [Enemy()]
    # items = [Item()]
    # electric_booms = []
    # big_drones = []
    # mini_drones = []
    # electric_balls = []
    # shurikens = []

    # enemies[0].Cal_rad()

    server.time_create_enemy = 0
    server.time_create_item = 100
    server.time_create_mdrone = 0

    server.num_create_mdrone = 0

# 게임 종료 - 객체를 소멸
def exit() :
    game_world.clear()

def update() :
    for game_object in game_world.all_objects():
        game_object.update()

    # for eboom in electric_booms :
    #     if eboom.update() == False :
    #         electric_booms.remove(eboom)

    # for bdrone in big_drones :
    #     if bdrone.update() == False :
    #         big_drones.remove(bdrone)

    # for mdrone in mini_drones :
    #     if mdrone.update() == False :
    #         mini_drones.remove(mdrone)

    # for eball in electric_balls :
    #     if eball.update() == False :
    #         electric_balls.remove(eball)

    # for shuriken in shurikens :
    #     if shuriken.update() == False :
    #         shurikens.remove(shuriken)

    # Add_Enemy()
    # Add_Item()
    # Add_Mdrone()
    # Chk_Drone_N_Enemy()
    # Chk_Drone_N_Item()
    # Chk_Eboom_N_Enemy()
    # Chk_Bdrone_N_Enemy()
    # Chk_Mdrone_N_Enemy()
    # Chk_Eball_N_Enemy()
    # Chk_Shuriken_N_Enemy()
    # Chk_Game_End()
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
    