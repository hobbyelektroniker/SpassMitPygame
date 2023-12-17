import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
from player import *
from others import *


class MyGame(pgt.Game):
    def __init__(self, title="Aliens", width=800, height=600, fps=60, fontsize=30, bgcolor='black'):
        super().__init__(title=title, width=width, height=height, fps=fps, fontsize=fontsize, bgcolor=bgcolor)

        zentrum = pgt.get_center()

        # Einige Sterne
        for _ in range(100):
            x = random.randint(5, width - 5)
            y = random.randint(5, height - 5)
            r = random.randint(1, 4)
            pg.draw.circle(self.background, color='white', center=(x, y), radius=r)

        # Punkte
        self.punkte = pgt.TraceVar(0)
        pgt.Label(self, pos=(width - 20, 20), anchor='tr', color='yellow', var=self.punkte)
        self.gameovertext = pgt.Label(self, pos=(zentrum.x, zentrum.y - 60), value='GAME OVER', anchor='c',
                                      color='yellow', fontsize=120, visible=False)
        self.starttext = pgt.Label(self, pos=zentrum, value='Neues Spiel mit Leertaste', anchor='c',
                                   color='yellow', fontsize=50, visible=True)

        self.raumschiff = Raumschiff(self, pos=(20, zentrum.y), anchor='lm')
        # Alien(self, pos=zentrum, anchor='c')

        # for _ in range(3):
        #     self.neues_alien()

        pgt.Media.load_sound('hit', 'hit.wav')
        pgt.Media.load_sound('gameover', 'loss.wav')
        pgt.Media.play_music('Soliloquy.mp3')

        # self.show_boxes(self.visible_sprites)

    def neues_spiel(self):
        self.gameovertext.visible = self.starttext.visible = False
        self.punkte.value = 0
        self.raumschiff.pos = (20, pgt.get_center().y)
        for _ in range(3):
            self.neues_alien()

    def game_over(self):
        pgt.Media.play_sound('gameover')
        self.gameovertext.visible = self.starttext.visible = True
        for alien in self.other_sprites:
            alien.kill()

    def neues_alien(self):
        breite, hoehe = pgt.get_size()
        pos = (breite + 100, random.randint(100, int(hoehe) - 100))
        Alien(self, pos=pos, anchor='c')

    def handle_event(self, event):
        super().handle_event(event)
        if self.starttext.visible and event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
            self.neues_spiel()

    def update(self, dt):
        super().update(dt)
        erwischt = self.raumschiff.collide_with_group(self.other_sprites, dokill=True)
        for _ in erwischt:
            pgt.Media.play_sound('hit')
            self.punkte.value += 1
            self.neues_alien()
        for alien in self.other_sprites:
            if alien.rect.right < 0:
                self.game_over()
                break


if __name__ == '__main__':
    MyGame().run()
