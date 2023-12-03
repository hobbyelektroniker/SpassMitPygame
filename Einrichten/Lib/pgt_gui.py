import pygame as pg
from pygame.locals import *
import pygame.sprite as sprite
import os
import math
import random
import pathlib
from pttools import *
import pgtools as pgt


def get_font(game, fontname=None, fontsize=None, font=None):
    if font:
        return font
    if fontname:
        return pg.font.Font(name=fontname, size=fontsize)
    if fontsize:
        return pg.font.Font(size=fontsize)
    else:
        return game.font


class Label(pgt.SpriteObject):
    def __init__(self, game, *, pos=(0, 0), value="X", fontsize=50, font=None, anchor='tl', color="white",
                 tcolor=(0, 0, 0), var_name=None, var=None, active=True, visible=True):
        super().__init__(game=game, pos=pos, anchor=anchor, tcolor=tcolor, active=active, visible=visible)

        self.value = value
        self.image = None
        self.var = None
        self.font = get_font(game, fontsize=fontsize, font=font)
        if var:
            self.var = var
            self.var.trace_add(self.update_value, mode='c')
        elif var_name:
            self.var = get_object(var_name)
            if self.var:
                self.var.trace_add(self.update_value, mode='c')
        if self.var:
            self.value = self.var.value
        self.color = color
        self.render()

    def update_value(self, *args):
        self.set_value(self.var.value)

    def render(self):
        pos = pgt.get_rect_pos(self.rect, self.anchor)
        self.image = pgt.create_text(text=str(self.value), font=self.font, color=self.color)
        self.rect = self.image.get_rect()
        pgt.set_rect_pos(self.rect, pos, self.anchor)

    def set_value(self, value):
        if value != self.value:
            self.value = value
            if self.active:
                self.render()



class Button(pgt.SpriteObject):
    def __init__(self, game, *, pos=(0, 0), size=(10, 10), text="Button", fontsize=50, font=None, anchor='tl',
                 color="white", bg_color='darkblue', tcolor=(0, 0, 0), func=None, active=True, visible=True):
        self.font = get_font(game, fontsize=fontsize, font=font)
        txt = pgt.create_text(text=text, font=self.font, antialias=True, color=color)
        w, h = txt.get_size()
        w += 20
        h += 10
        size = pgt.Size(size)
        if size.w < w:
            size.w = w
        if size.h < h:
            size.h = h
        super().__init__(game=game, pos=pos, size=size, anchor=anchor, tcolor=tcolor, active=active, visible=visible)
        self._text = text
        self.color = color
        self.tag = None
        self.size = size
        self.bg_color = bg_color
        self.hot = False
        self.func = func
        self.render()
        self.eventvar = self.game.app_event
        self.eventvar.trace_add(self.on_event)

    def render(self):
        txt = pgt.create_text(text=self._text, font=self.font, antialias=True, color=self.color)
        self.image.fill(self.tcolor)
        if not self.enabled:
            col = 'darkgray'
        elif self.hot:
            col = 'blue'
        else:
            col = self.bg_color
        pg.draw.rect(self.image, color=col, rect=(0, 0, self.size.w, self.size.h), border_radius=int(self.size.h // 4))
        text_rect = txt.get_rect()
        text_rect.center = self.image.get_rect().center
        self.image.blit(txt, dest=text_rect.topleft)

    def update(self, dt):
        super().update(dt)

    def on_event(self, tag=None):
        event = self.eventvar.value
        if not event: return
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.enabled:
                if self.func:
                    self.func(self)
        if event.type == pg.MOUSEMOTION and self.rect.collidepoint(event.pos):
            if not self.hot:
                self.hot = True
                self.render()
        else:
            if self.hot:
                self.hot = False
                self.render()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.render()

    @property
    def enabled(self):
        return self.active

    @enabled.setter
    def enabled(self, value):
        self.active = value
        self.render()


class Checkbox(pgt.SpriteObject):
    def __init__(self, game, *, pos=(0, 0), size=(10, 10), text="Checkbox", fontsize=50, font=None, anchor='tl',
                 color="white", bg_color='darkblue', tcolor=(0, 0, 0), func=None, active=True, visible=True,
                 checked=False, tag=None):
        self.font = get_font(game, fontsize=fontsize, font=font)
        txt = pgt.create_text(text=text, font=self.font, antialias=True, color=color)
        w, h = txt.get_size()
        w += 50
        h += 10
        size = pgt.Size(size)
        if size.w < w:
            size.w = w
        if size.h < h:
            size.h = h
        super().__init__(game=game, pos=pos, size=size, anchor=anchor, tcolor=tcolor, active=active, visible=visible)
        self._text = text
        self.color = color
        self.bg_color = bg_color
        self.tag = tag
        self.size = size
        self.hot = False
        self._checked = checked
        self.func = func
        self.render()
        self.eventvar = self.game.app_event
        self.eventvar.trace_add(self.on_event)

    def render(self):
        self.image.fill(self.tcolor)
        if not self.enabled:
            col = 'darkgray'
        elif self.hot:
            col = 'blue'
        else:
            col = self.bg_color
        txt = pgt.create_text(text=self._text, font=self.font, antialias=True, color=self.color)
        l = self.size.h - 4
        pg.draw.rect(self.image, color=col, rect=(0, 0, l, l))
        padding = 10
        if self.checked:
            pg.draw.line(self.image, color=self.color, start_pos=(padding-1, padding-1), end_pos=(l-padding-1, l-padding-1), width=2)
            pg.draw.line(self.image, color=self.color, start_pos=(l-padding-1, padding-1), end_pos=(padding-1, l-padding-1), width=2)
        text_rect = txt.get_rect()
        text_rect.midleft = (l + 5, l//2)
        self.image.blit(txt, dest=text_rect.topleft)

    def update(self, dt):
        super().update(dt)

    def on_event(self, tag=None):
        event = self.eventvar.value
        if not event: return
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos) and self.enabled:
                self.checked = not self.checked
                self.render()
                if self.func:
                    self.func(self)
        if event.type == pg.MOUSEMOTION and self.rect.collidepoint(event.pos):
            if not self.hot:
                self.hot = True
                self.render()
        else:
            if self.hot:
                self.hot = False
                self.render()

    @property
    def checked(self):
        return self._checked

    @checked.setter
    def checked(self, value):
        self._checked = value
        self.render()

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        self.render()

    @property
    def enabled(self):
        return self.active

    @enabled.setter
    def enabled(self, value):
        self.active = value
        self.render()
