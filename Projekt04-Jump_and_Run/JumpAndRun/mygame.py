import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
from player import *
from others import *

class MyGame(pgt.Game):
    def __init__(self, title="Jump and Run", width=800, height=600, fps=60, fontsize=30, bgcolor='black'):
        super().__init__(title=title, width=width, height=height, fps=fps, fontsize=fontsize, bgcolor=bgcolor)

        # lokale Variablen
        himmel = 400  # y - Koordinate der Grenze zwischen Himmel und Boden
        farbe_himmel = (163, 232, 254)
        farbe_boden = (88, 242, 152)

        # verschiedene Eigenschaften des Spiels
        self.active = False             # Das Spiel ist noch nicht aktiv
        self.speed = 150                # Das ist die Startgeschwindigkeit
        self.fusslinie = himmel + 50    # Die Fusslinie aller Spielobjekte

        # Hintergrund
        self.background.fill(farbe_himmel)
        pg.draw.rect(self.background, color=farbe_boden, rect=(0, himmel, width, height - himmel))

        # Punktezähler
        self.punkte = pgt.TraceVar(0)
        pgt.Label(self, pos=(width - 80, 20), fontsize=60, anchor='tr', var=self.punkte)

        # Spieler und Kakteen vorbereiten
        self.spieler = None
        self.kaktus_gruppe = self.create_group()
        self.kaktus = None      # der zuletzt erzeugte Kaktus
        self.kaktus_x = None    # Wenn der zuletzt erzeugte Kaktus links davon ist, wird ein neuer erzeugt

        # Sounds laden
        pgt.Media.load_sound('gameover', 'gameover.wav')

        self.function(3, self.schneller)
        # self.show_boxes(self.visible_sprites)

        self.neues_spiel()

    def neues_spiel(self):
        # alte Spieler und Kakteen zerstören
        if self.spieler:
            self.spieler.kill()
        for kaktus in self.kaktus_gruppe:
            kaktus.kill()

        # Der Spieler und der ersten Kaktus wird erzeugt
        self.spieler = self.neuer_spieler()
        self.neuer_kaktus()

        # Punkte und Geschwindigkeit
        self.punkte.value = 0
        self.speed = 150

        # Hintergrundmusik
        pgt.Media.play_music('venus.wav')


        self.active = True

    def schneller(self):
        if self.active:
            self.speed += 20

    def neuer_spieler(self):
        spieler = Spieler(self, pos=(100, self.fusslinie), anchor='bl')
        # spieler = Spieler(self, pos=(100, 200), anchor='bl')
        spieler.animating = True
        spieler.constraints(top=10, bottom=self.fusslinie)
        return spieler

    def neuer_kaktus(self):
        self.kaktus = Kaktus(self, pos=(pgt.get_width(), self.fusslinie), anchor='bl', group=self.kaktus_gruppe)
        self.kaktus_x = pgt.get_width() - random.randint(300, 800)

    def handle_event(self, event):
        super().handle_event(event)
        if event.type == pg.KEYDOWN:
            # if event.key == pg.K_KP_PLUS:
            #     self.speed += 20
            # elif event.key == pg.K_KP_MINUS:
            #     self.speed -= 20
            if event.key == pg.K_RETURN:
                if not self.active:
                    self.neues_spiel()

    def game_over(self):
        pgt.Media.pause_music()
        pgt.Media.play_sound('gameover')
        self.active = False
        for kaktus in self.kaktus_gruppe:
            kaktus.active = False

    def update(self, dt):
        super().update(dt)
        if self.active:
            kollisionen = self.spieler.collide_with_group(self.kaktus_gruppe)
            if kollisionen:
                kollisionen[0].hit()
                self.spieler.hit()
                self.game_over()
            elif self.kaktus.rect.left < self.kaktus_x:
                self.neuer_kaktus()

if __name__ == '__main__':
    MyGame().run()

