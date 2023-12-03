import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
from datetime import datetime


class MyGame(pgt.Game):
    def __init__(self, title="Eine Uhr", width=600, height=600, fps=60, fontsize=30, bgcolor='blue'):
        super().__init__(title=title, width=width, height=height, fps=fps, fontsize=fontsize, bgcolor=bgcolor)

        # Standardfont ersetzen
        self.font = pg.font.SysFont("arial", 40, bold=True)

        # Zentrum und Radius der Uhr
        self.zentrum = pgt.get_center()
        self.radius = width // 2 - 50

        # Uhr in den Hintergrund zeichnen
        pg.draw.circle(self.background, color='white', center=self.zentrum, radius=10)  # Zeigerachse
        pg.draw.circle(self.background, color='white', center=self.zentrum, radius=self.radius, width=3)

        for winkel in range(6, 361, 6):
            aussen = pgt.Position.from_deg(winkel - 90, length=self.radius - 2, center=self.zentrum)
            innen = pgt.Position.from_deg(winkel-90, self.radius-10, self.zentrum)
            stunde = pgt.Position.from_deg(winkel-90, self.radius-30, self.zentrum)
            ziffer = pgt.Position.from_deg(winkel-90, self.radius-60, self.zentrum)

            if winkel % 30 == 0:
                # Stundenstrich
                pg.draw.line(self.background, color='white', start_pos=aussen, end_pos=stunde, width=3)
                pgt.draw_text(self.background, text=winkel // 30, font=self.font, pos=ziffer, anchor='c')
            else:
                # Minutenstrich
                pg.draw.line(self.background, color='white', start_pos=aussen, end_pos=innen, width=3)

        # Labels für digitale Anzeige von Datum und Zeit
        self.datum_label = pgt.Label(self, pos=(20, height - 15), value="01.01.2023", anchor='bl')
        self.zeit_label = pgt.Label(self, pos=(width - 20, height - 15), value="00:00:00", anchor='br')

        # aktuelle Zeit
        self.zeit = datetime.now()

    def sekundenzeiger(self):
        winkel = 360 / 60 * self.zeit.second
        # winkel += 360 / 60 / 1_000_000 * self.zeit.microsecond
        r = self.radius - 90
        aussen = pgt.Position.from_deg(winkel-90, r, self.zentrum)
        pg.draw.line(self.screen, color='white', start_pos=aussen, end_pos=self.zentrum, width=2)

    def minutenzeiger(self):
        winkel = 360 / 60 * self.zeit.minute + 360 / 60 / 60 * self.zeit.second
        r = self.radius - 40
        aussen = pgt.Position.from_deg(winkel-90, r, self.zentrum)
        pg.draw.line(self.screen, color='white', start_pos=aussen, end_pos=self.zentrum, width=4)

    def stundenzeiger(self):
        winkel = 360 / 12 * self.zeit.hour + 360 / 12 / 60 * self.zeit.minute + 360 / 12 / 60 / 60 * self.zeit.second
        r = self.radius - 100
        aussen = pgt.Position.from_deg(winkel-90, r, self.zentrum)
        pg.draw.line(self.screen, color='white', start_pos=aussen, end_pos=self.zentrum, width=4)

    def update(self, dt):
        super().update(dt)
        self.zeit = datetime.now()
        self.datum_label.set_value(self.zeit.strftime("%d.%m.%Y"))
        self.zeit_label.set_value(self.zeit.strftime("%H:%M:%S"))

    def draw(self):
        super().draw()
        self.sekundenzeiger()
        self.minutenzeiger()
        self.stundenzeiger()


if __name__ == '__main__':
    MyGame().run()


