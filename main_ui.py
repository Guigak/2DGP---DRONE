from pico2d import *
import game_framework
import play_state

import server

class Main_Ui :
    image = None
    font = None

    def __init__(self):
        if Main_Ui.image == None :
            Main_Ui.image = load_image('./resource/main.png')
        if Main_Ui.font == None :
            Main_Ui.font = load_font('./resource/H2HDRM.TTF', 50)

        self.num_selected = 0   # 0 - start / 1 - exit

    def update(self) :
        pass

    def draw(self):
        self.image.draw(server.WIDTH // 2, server.HEIGHT // 2)

        if self.num_selected == 0:
            self.font.draw(433, 300, 'START', (127, 0, 0))
            self.font.draw(455, 150, 'EXIT', (255, 255, 255))
        else :
            self.font.draw(433, 300, 'START', (255, 255, 255))
            self.font.draw(455, 150, 'EXIT', (127, 0, 0))

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN :
            if event.key == SDLK_UP:
                self.num_selected -= 1

                if self.num_selected == -1 :
                    self.num_selected += 2
            if event.key == SDLK_DOWN :
                self.num_selected = (self.num_selected + 1) % 2
            if event.key == SDLK_RETURN :
                match self.num_selected :
                    case 0:
                        server.map_y = server.map.move_y
                        game_framework.change_state(play_state)
                    case 1:
                        game_framework.quit()
                    case _:
                        pass
