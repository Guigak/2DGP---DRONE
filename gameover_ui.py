from pico2d import *
import game_framework
import main_state
import play_state

import server

class Gameover_Ui :
    image = None
    sound = None
    font = None

    def __init__(self):
        if Gameover_Ui.image == None :
            Gameover_Ui.image = load_image('./resource/gameover_r.png')
        if Gameover_Ui.sound == None :
            Gameover_Ui.sound = load_wav('./resource/gameover_sound.wav')
        if Gameover_Ui.font == None :
            Gameover_Ui.font = load_font('./resource/H2HDRM.TTF', 50)

        self.sound.set_volume(32)
        self.sound.play()

        self.num_selected = 0   # 0 - start / 1 - exit

    def update(self) :
        pass

    def draw(self):
        server.map.draw_gameover()
        server.drone.draw_gameover()

        for enemy in server.enemies :
            enemy.draw_gameover()
        
        self.image.draw(server.WIDTH // 2, server.HEIGHT // 2)
        
        self.font.draw(150, 400, 'SCORE : %d' % server.score.num_score, (257, 257, 257))

        if self.num_selected == 0:
            self.font.draw(433, 300, 'RETRY', (127, 0, 0))
            self.font.draw(444, 150, 'MAIN', (255, 255, 255))
        else :
            self.font.draw(433, 300, 'RETRY', (255, 255, 255))
            self.font.draw(444, 150, 'MAIN', (127, 0, 0))

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
                        server.drone.reset_flag()
                        game_framework.pop_state()
                        game_framework.change_state(play_state)
                    case 1:
                        game_framework.pop_state()
                        game_framework.change_state(main_state)
                    case _:
                        pass
