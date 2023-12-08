import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
from player import *
from others import *


class MyGame(pgt.Game):
    def __init__(self, title="Monkey Fever", width=1280, height=480, fps=60, fontsize=64, bgcolor=(170, 238, 197)):
        super().__init__(title=title, width=width, height=height, fps=fps, fontsize=fontsize, bgcolor=bgcolor)

        # pg.mouse.set_visible(False)
        zentrum = pgt.get_center()
        pos = (zentrum.x, 10)
        pgt.draw_text(self.background, text="Pummel The Chimp, And Win $$$", pos=pos, anchor='tm',
                      font=self.font, color=(10, 10, 10))

        pgt.Media.load_sound("whiff", "whiff.wav")
        pgt.Media.load_sound("punch", "punch.wav")

        self.fist = Fist(self, pos=zentrum, anchor='tr')
        self.chimp_gruppe = self.create_group()
        Chimp(self, pos=(0, 120), anchor='tr', group=self.chimp_gruppe)
        # Chimp(self, pos=(200, 120), anchor='tr', group=self.chimp_gruppe)
        # Chimp(self, pos=(pgt.get_width()+1, 120), anchor='tl', group=self.chimp_gruppe)

        # self.show_boxes(self.player_sprites, self.chimp_gruppe)

    def update(self, dt):
        super().update(dt)
        if self.fist.punching:
            treffer = self.fist.collide_with_group(self.chimp_gruppe)
            for chimp in treffer:
                chimp.spin()


if __name__ == '__main__':
    MyGame().run()

