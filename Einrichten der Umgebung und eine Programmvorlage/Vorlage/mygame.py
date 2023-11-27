import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
from player import *
from others import *

class MyGame(pgt.Game):
    def __init__(self, title="Mein Spiel", width=800, height=600, fps=60, fontsize=30, bgcolor='black'):
        super().__init__(title=title, width=width, height=height, fps=fps, fontsize=fontsize, bgcolor=bgcolor)

        # Beispielcode
        # Hintergrund
        size = pgt.Size(self.background.get_size()) // 2
        center = pgt.get_center(self.background)

        rect = Rect(0, 0, size.w, size.h)
        pgt.set_rect_pos(rect, center, 'c')
        pg.draw.rect(self.background, color='yellow', rect=rect)

        # Ein rechteckiger Spieler
        self.spieler = Spieler(self, pos=center, size=(50, 50), anchor='c')
        self.spieler.constraints(top=rect.top, bottom=rect.bottom, left=rect.left, right=rect.right)

        # Drei runde Gegner
        self.gegner_gruppe = sprite.Group()
        for i in range(3):
            gegner = Gegner(self, pos=center - (150, random.randint(50, 300)), size=(50, 50),
                            group=self.gegner_gruppe)
            gegner.speed = 300
            gegner.keyboard_move(up=pg.K_a, down=pg.K_y)

    def handle_event(self, event):
        super().handle_event(event)

    def update(self, dt):
        super().update(dt)

        # Beispielcode
        sprite.spritecollide(self.spieler, self.gegner_gruppe, dokill=True)

    def draw(self):
        super().draw()

if __name__ == '__main__':
    MyGame().run()

