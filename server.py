map = None
main_ui = None
drone = None
enemies = None
items = None
electric_booms = None
big_drones = None
mini_drones = None
electric_balls = None
shurikens = None

score = None

pause = None

time_create_enemy = None
time_create_item = None
time_create_mdrone = None

num_create_mdrone = None

HEIGHT = None
WIDTH = None

map_y = None



objects = [map, main_ui, drone, enemies, items, electric_booms, big_drones, mini_drones, electric_balls, shurikens, pause, score]

def all_clear() :
    global map, main_ui, drone, enemies, items, electric_booms, big_drones, mini_drones, electric_balls, shurikens,\
        pause, score, time_create_enemy, time_create_item, time_create_mdrone, num_create_mdrone

    for i in range(len(objects)) :
        remove_object(objects[i])

    map = None
    main_ui = None
    drone = None
    enemies = None
    items = None
    electric_booms = None
    big_drones = None
    mini_drones = None
    electric_balls = None
    shurikens = None

    score = None

    pause = None

    time_create_enemy = None
    time_create_item = None
    time_create_mdrone = None

    num_create_mdrone = None

def remove_object(t) :
    for t in objects :
        if type(t) != type(None) and type(t) == type([]):
            t.remove(t[len(t) - 1])