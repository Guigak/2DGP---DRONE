
# 0 - map / 1 - enemy / 2 - drone / 3 - item / 4 - e_boom / 5 - shuriken / 6 - b_drone / 7 - m_drone / 8 - e_ball / 9 - pause
objects = [[], [], [], [], [], [], [], [], [], []]
collision_group = dict()

def add_object(o, depth):
    objects[depth].append(o)

def add_objects(ol, depth):
    objects[depth] += ol

def remove_object(o):
    for layer in objects:
        try:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
        except:
            pass
    raise ValueError('Trying destroy non existing object')


def all_objects():
    for layer in objects:
        for o in layer:
            yield o


def clear():
    target_objects = objects

    for target_layer in target_objects:
        if target_layer :
            for i in range(len(target_layer)) :
                remove_object(target_layer[0])





def add_collision_pairs(a, b, group):

    if group not in collision_group:
        print('Add new group ', group)
        collision_group[group] = [ [], [] ] # list of list : list pair

    if a:
        if type(a) is list:
            collision_group[group][0] += a
        else:
            collision_group[group][0].append(a)

    if b:
        if type(b) is list:
            collision_group[group][1] += b
        else:
            collision_group[group][1].append(b)

    print(collision_group)

def add_collision(o, l, group) :
    if group in collision_group :
        if type(o) is list:
            collision_group[group][l] += o
        else:
            collision_group[group][l].append(o)   
        
        print(collision_group)


def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group


def remove_collision_object(o):
    for pairs in collision_group.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def update():
    for game_object in all_objects():
        game_object.update()


