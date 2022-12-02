from pico2d import *

class Score :
    font = None

    def __init__(self):
        if Score.font == None :
            Score.font = load_font('./resource/H2HDRM.TTF', 50)

        self.num_score = 0

    def update(self) :
        if self.num_score > 100 :
            self.num_score += 1

    def draw(self):
        self.font.draw(25, 850, 'SCORE : %d' % self.num_score, (257, 257, 257))

    def add_score(self) :
        self.num_score += 5