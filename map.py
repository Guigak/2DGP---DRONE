class Map :
    image = None

    def __init__(self):
        if Map.image == None :
            Map.image = load_image('map.png')
        self.speed = 10
        self.move_y = 0

    def draw(self):
        self.image.draw(WIDTH // 2, HEIGHT // 2 - self.move_y)
        self.image.draw(WIDTH // 2, HEIGHT // 2 + HEIGHT - self.move_y)

        self.move_y = (self.move_y + self.speed) % HEIGHT
