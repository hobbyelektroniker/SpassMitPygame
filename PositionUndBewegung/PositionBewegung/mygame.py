import random
import pygame as pg
import pygame.sprite as sprite
from pygame.locals import *
import pgtools as pgt
from player import *
from others import *


class MyGame(pgt.Game):
    def __init__(self, title="Positionierung und Bewegung", width=2000, height=1300, fps=60, fontsize=20,
                 bgcolor='black'):
        super().__init__(title=title, width=width, height=height, fps=fps, fontsize=fontsize, bgcolor=bgcolor)

        zentrum = pgt.get_center()
        x = 0
        while x < width:
            if x % 100 == 0:
                y = 20
                if x > 0:
                    pgt.draw_text(self.background, text=x, pos=(x, y + 10), font=self.font, color='white', anchor='tm')
            elif x % 50 == 0:
                y = 10
            else:
                y = 5
            pg.draw.line(self.background, color='white', start_pos=(x, 0), end_pos=(x, y), width=1)
            x += 10

        y = 0
        while y < height:
            if y % 100 == 0:
                x = 20
                if y > 0:
                    pgt.draw_text(self.background, text=y, pos=(x + 10, y), font=self.font, color='white', anchor='lm')
            elif y % 50 == 0:
                x = 10
            else:
                x = 5
            pg.draw.line(self.background, color='white', start_pos=(0, y), end_pos=(x, y), width=1)
            y += 10

        self.text_font = pg.font.SysFont('arial', 30)
        self.show_boxes(self.player_sprites)

        self.anchors = ['tl', 'tm', 'tr', 'ml', 'c', 'mr', 'bl', 'bm', 'br']
        self.anchor_idx = 0
        self.anchor = self.anchors[self.anchor_idx]  # 'tl'

        self.info = f"set_anchor('{self.anchor}')"

        pos = (400, 600)
        # pos = pgt.Position(400, 600)
        # pos = pgt.Position.from_deg(deg=30, length=600)
        self.spieler = Spieler(self, pos=pos, anchor=self.anchor, size=(200, 200))
        self.spieler.constraints(top=300, bottom=pgt.get_height(), left=60, right=pgt.get_width())
        self.constrain_txt = f"constraints(top=300, bottom={pgt.get_height()}, left=60, right={pgt.get_width()})"

        pgt.Button(self, pos=(750, 50), size=(320, 40), text=f"set_anchor(); anchor=", anchor='tr', font=self.text_font,
                   func=self.set_anchor)
        pgt.Button(self, pos=(750, 100), size=(320, 40), text=f"change_anchor()", anchor='tr', font=self.text_font,
                   func=self.change_anchor)

        pgt.draw_text(self.background, text='speed', pos=(1020, 50), anchor='tr', color='yellow', font=self.text_font)
        self.speedvar = pgt.TraceVar(50)
        pgt.Slider(self, pos=(1025, 53), color='yellow', size=(250, 30), value_range=(-50, 550), var=self.speedvar)
        pgt.Label(self, pos=(1300, 50), color='yellow', var=self.speedvar, str_format="{:0.0f}")

        pgt.draw_text(self.background, text='direction.deg', pos=(1020, 100), anchor='tr', color='yellow',
                      font=self.text_font)
        self.degvar = pgt.TraceVar(0)
        pgt.Slider(self, pos=(1025, 103), color='yellow', size=(250, 30), value_range=(-90, 450), var=self.degvar)
        pgt.Label(self, pos=(1300, 100), color='yellow', var=self.degvar, str_format="{:0.0f}")

        sz = (120, 40)
        pgt.Button(self, pos=(1380, 95), size=sz, text=".right()", font=self.text_font, func=self.direction_button)
        pgt.Button(self, pos=(1520, 95), size=sz, text=".down()", font=self.text_font, func=self.direction_button)
        pgt.Button(self, pos=(1660, 95), size=sz, text=".left()", font=self.text_font, func=self.direction_button)
        pgt.Button(self, pos=(1800, 95), size=sz, text=".up()", font=self.text_font, func=self.direction_button)

        self.auto = pgt.Checkbox(self, pos=(850, 150), text="Selbstständige Bewegung", font=self.text_font,
                                 color='yellow', tag='auto', checked=False, func=self.cb_changed)
        self.kb = pgt.Checkbox(self, pos=(850, 185),
                               text="keyboard_move(left=K_LEFT, right=K_RIGHT, up=K_UP, down=K_DOWN)",
                               font=self.text_font, color='yellow', tag='kb', checked=False, func=self.cb_changed)
        self.mouse = pgt.Checkbox(self, pos=(850, 220), text="mouse_move = True",
                                  font=self.text_font, color='yellow', tag='ms', checked=False, func=self.cb_changed)
        self.speedvar.trace_add(self.move_changed, 'c')
        self.degvar.trace_add(self.move_changed, 'c')

        self.spieler.speed = self.speedvar.value


    def move_changed(self, *args):
        self.spieler.speed = self.speedvar.value
        if self.auto.checked:
            self.spieler.direction.deg = self.degvar.value
        else:
            self.spieler.direction.clear()
        if self.kb.checked:
            self.spieler.keyboard_move(left=K_LEFT, right=K_RIGHT, up=K_UP, down=K_DOWN)
        else:
            self.spieler.keyboard_move()
        self.spieler.mouse_move = self.mouse.checked

    def direction_button(self, button):
        deg = 0
        if button.text == '.right()': deg = 0
        if button.text == '.down()': deg = 90
        if button.text == '.left()': deg = 180
        if button.text == '.up()': deg = 270
        self.degvar.value = deg

    def cb_changed(self, button):
        if button.tag == 'auto':
            self.kb.checked = False
            self.mouse.checked = False
            self.move_changed()
        elif button.tag == 'kb':
            self.auto.checked = False
            self.mouse.checked = False
            self.move_changed()
        elif button.tag == 'ms':
            self.auto.checked = False
            self.kb.checked = False
            self.move_changed()

    def next_anchor(self):
        if self.anchor_idx is None or self.anchor_idx == len(self.anchors) - 1:
            self.anchor_idx = 0
        else:
            self.anchor_idx += 1
        self.anchor = self.anchors[self.anchor_idx]

    def set_anchor(self, tag=None):
        self.next_anchor()
        # self.spieler.set_anchor(self.anchor)
        self.spieler.anchor = self.anchor
        self.info = f"set_anchor('{self.anchor}')"

    def change_anchor(self, tag=None):
        self.next_anchor()
        self.spieler.change_anchor(self.anchor)
        self.info = f"change_anchor('{self.anchor}')"

    def handle_event(self, event):
        if event.type == KEYDOWN:
            if event.key == K_s:
                self.set_anchor()
            elif event.key == K_c:
                self.change_anchor()

    def print(self, line, text1, text2=None):
        pos = pgt.Position(70, 50 + 30 * line)
        if line > 1: pos.y += 15
        pgt.draw_text(self.screen, text=text1, pos=pos, font=self.text_font, color='yellow')

    def draw(self):
        super().draw()
        self.print(0, f"pos = ({self.spieler.pos.x}, {self.spieler.pos.y})")
        # self.print(1, f"anchor = '{self.spieler.anchor}', mit {self.info}")
        self.print(1, f"anchor = '{self.spieler.anchor}'", text2=f"(mit {self.info})")

        r = self.spieler.rect
        self.print(2, f"rect.size = {self.spieler.rect.size}")
        self.print(3, f"rect.left = {self.spieler.rect.left}, rect.centerx = {self.spieler.rect.centerx}, "
                      f"rect.right = {self.spieler.rect.right}")
        self.print(4, f"rect.top = {self.spieler.rect.top}, rect.centery = {self.spieler.rect.centery}, "
                      f"rect.bottom = {self.spieler.rect.bottom}")

        self.print(6, self.constrain_txt)

        p = self.spieler.pos
        pg.draw.line(self.screen, color='yellow', start_pos=(p.x - 10, p.y), end_pos=(p.x + 10, p.y), width=1)
        pg.draw.line(self.screen, color='yellow', start_pos=(p.x, p.y - 10), end_pos=(p.x, p.y + 10), width=1)

        c = self.spieler.rect.center
        p = pgt.Position.from_deg(self.degvar.value, length=250, center=c)
        pg.draw.line(self.screen, color='yellow', start_pos=self.spieler.rect.center, end_pos=p, width=1)

        p1 = pgt.Position.from_deg(self.degvar.value - 2, length=225, center=c)
        p2 = pgt.Position.from_deg(self.degvar.value + 2, length=225, center=c)
        pg.draw.line(self.screen, color='yellow', start_pos=p, end_pos=p1, width=1)
        pg.draw.line(self.screen, color='yellow', start_pos=p, end_pos=p2, width=1)


if __name__ == '__main__':
    MyGame().run()
