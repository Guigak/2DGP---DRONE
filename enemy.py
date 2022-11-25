class Enemy :
    image = None
    radius = 50

    def __init__(self):
        if Enemy.image == None :
            Enemy.image = load_image('enemy.png')
        #self.radius = 50
        self.default_x = self.position_x = random.randint(0, WIDTH)
        self.default_y = self.position_y = HEIGHT + self.radius

        self.speed = random.randint(3, 5)
        self.time = 0

        self.rad = 0
        self.reverse = False

        self.alive = True

        self.frame_x = 0
        self.frame_y = 0

    def update(self):
        if self.reverse :
            self.position_x = self.default_x - self.speed * self.time * math.cos(self.rad)
            self.position_y = self.default_y - self.speed * self.time * math.sin(self.rad)
        else :
            self.position_x = self.default_x + self.speed * self.time * math.cos(self.rad)
            self.position_y = self.default_y + self.speed * self.time * math.sin(self.rad)

        self.time += 1

        if (self.position_x < -self.radius) or (self.position_x > WIDTH + self.radius) :
            self.alive = False

        if self.position_y < -self.radius :
            self.alive = False

        if not self.alive :
            self.default_x = random.randint(0, WIDTH)
            self.reverse = False
            self.Cal_rad()
            self.time = 0

            self.alive = True

    def draw(self):
        self.image.clip_composite_draw(self.radius * 2 * self.frame_x, self.frame_y,\
                                        self.radius * 2, self.radius * 2,\
                                        self.rad, 'n',\
                                        self.position_x, self.position_y,\
                                        self.radius * 2, self.radius * 2)

        self.frame_x = (self.frame_x + 1) % 2

    def Cal_rad(self) :
        dx = drone.position_x - self.default_x
        dy = drone.position_y - self.default_y

        if dx < 0 :
            self.reverse = True

        if dx == 0 :
            self.rad = math.atan(dy / 1)
        else :
            self.rad = math.atan(dy / dx)

    def Chk_with_Drone(self) :
        tum_x = drone.position_x - self.position_x
        tum_y = drone.position_y - self.position_y

        tum = math.sqrt(tum_x ** 2 + tum_y ** 2)

        if tum < self.radius + drone.radius :
            if drone.shield :
                self.alive = False
            else :
                drone.alive = False
        pass