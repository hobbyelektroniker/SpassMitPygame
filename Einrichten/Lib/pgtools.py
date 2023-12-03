import pygame as pg
from pygame.locals import *
import pygame.sprite as sprite
import os
import math
import random
import pathlib
from pttools import *
from pgt_gameclass import *
from pgt_gameobject import *
from pgt_gui import *
from pgt_media import *


"""
*** Hilfsfunktionen ***
- pixels_to_move(direction: pg.Vector2, speed: float, seconds: float) -> pg.Vector2
- get_rect_pos(rect: Rect, anchor='tl') -> Position
- set_rect_pos(rect: Rect, pos, anchor='mm')
- get_size(surface=None) -> Size
- get_width(surface=None) -> float
- get_height(surface=None) -> float
- get_center(surface=None) -> float
- get_mouse_pos() -> Position
- create_text(text, font, antialias=False, color='white', background=None) -> Surface

aus pttools.py
- register_object(name, obj, overwrite=False, no_error=False) 
- unregister_object(name)
- get_object(name, default=None) -> Any


*** Klassen ***
- Size(w, h)
- Position(x, y)
- Direction(x=0, y=0, deg=None, rad=None)

aus pttools.py
- Record(*args, **kwargs)
- TraceVar(value=None)

aus pgt_gameclass.py
- Function(seconds, func, loops=None, **kwargs)
- Game(title=" ", *, width=300, height=200, fps=60, fontsize=30, bgcolor='black')

aus pgt_gameobject.py
- SpriteObject(game, *, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True, tcolor=(0, 0, 0))
- GameObject(game, *, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True, tcolor=(0, 0, 0))

aus pgt_gui.py
- Label(game, *, pos=(0, 0), value="X", fontsize=50, font=None, anchor='tl', color="white",
         tcolor=(0, 0, 0), var_name=None, var=None, active=True, visible=True)

aus pgt_media.py
Media  (Klasse ohne Instanz)
- Media.load_image(filename, size=None, width=None, height=None, colorkey=None, createfullname=True)
- Media.load_images(filename, size=None, width=None, height=None, colorkey=None)
- Media.load_sound(name, filename)
- Media.set_soundvolume(volume) # 0.0 .. 1.0
- Media.play_sound(name, volume=None) # 0.0 .. 1.0
- Media.play_music(filename)
- Media.set_volume(volume) # 0.0 .. 1.0
- Media.pause_music()
- Media.unpause_music()
- Media.stop_music()


"""

def hitbox_collide(sprite, other):
    return sprite.hitbox().colliderect(other.hitbox())

def pixels_to_move(direction: pg.Vector2, speed: float, seconds: float) -> pg.Vector2:
    return direction * speed * seconds

def set_rect_pos(rect: Rect, pos, anchor='mm'):
    if anchor in ('bl', 'lb'):
        rect.bottomleft = pos
    elif anchor in ('bm', 'mb'):
        rect.midbottom = pos
    elif anchor in ('br', 'rb'):
        rect.bottomright = pos
    elif anchor in ('ml', 'lm'):
        rect.midleft = pos
    elif anchor in ('mm', 'c'):
        rect.center = pos
    elif anchor in ('mr', 'rm'):
        rect.midright = pos
    elif anchor in ('tl', 'lt'):
        rect.topleft = pos
    elif anchor in ('tm', 'mt'):
        rect.midtop = pos
    elif anchor in ('tr', 'rt'):
        rect.topright = pos
    else:
        rect.bottomleft = pos


def get_rect_pos(rect: Rect, anchor='tl'):
    if anchor in ('bl', 'lb'):
        pos = rect.bottomleft
    elif anchor in ('bm', 'mb'):
        pos = rect.midbottom
    elif anchor in ('br', 'rb'):
        pos = rect.bottomright
    elif anchor in ('ml', 'lm'):
        pos = rect.midleft
    elif anchor in ('mm', 'c'):
        pos = rect.center
    elif anchor in ('mr', 'rm'):
        pos = rect.midright
    elif anchor in ('tl', 'lt'):
        pos = rect.topleft
    elif anchor in ('tm', 'mt'):
        pos = rect.midtop
    elif anchor in ('tr', 'rt'):
        pos = rect.topright
    else:
        pos = rect.topleft
    return Position(pos)

class Size(pg.Vector2):
    def __str__(self):
        return f"Size: w={self.w}, h={self.h}"

    def __init__(self, w, h=None):
        super().__init__(w, h)

    @property
    def w(self):
        return self.x

    @w.setter
    def w(self, value):
        self.x = value

    @property
    def h(self):
        return self.y

    @h.setter
    def h(self, value):
        self.y = value


class Position(pg.Vector2):
    def __str__(self):
        return f"Position: x={self.x}, y={self.y}"

    @classmethod
    def from_deg(cls, deg, length=1, center=(0, 0)):
        return cls.from_polar((length, deg)) + center

    @classmethod
    def from_rad(cls, rad, radius=1, center=(0, 0)):
        deg = math.degrees(rad)
        return cls.from_deg(deg, radius, center)

    @property
    def length(self):
        return super().length()

    @length.setter
    def length(self, value):
        self.scale_to_length(value)

    @property
    def deg(self):
        r, phi = self.as_polar()
        return phi

    @deg.setter
    def deg(self, value):
        self.from_polar((self.length, value))

    @property
    def rad(self):
        r, phi = self.as_polar()
        return math.radians(phi)

    @rad.setter
    def rad(self, value):
        self.from_polar((self.length, math.degrees(value)))



class Direction(pg.Vector2):
    def __str__(self):
        return f"Direction: x={self.x}, y={self.y}, deg={self.deg}, rad={self.rad}"

    def __init__(self, x=0, y=0, deg=None, rad=None):
        super().__init__(x, y)
        if deg:
            self.deg = deg
        elif rad:
            self.rad = rad
        elif self.length():
            self.normalize_ip()

    def clear(self):
        self.xy = pg.Vector2(0, 0)

    @property
    def rad(self):
        r, phi = self.as_polar()
        return math.radians(phi)

    @rad.setter
    def rad(self, value):
        self.from_polar((1, math.degrees(value)))

    @property
    def deg(self):
        r, phi = self.as_polar()
        return phi

    @deg.setter
    def deg(self, value):
        self.from_polar((1, value))

def get_size(surface=None):
    if surface:
        return Size(surface.get_size())
    else:
        return Size(pg.display.get_surface().get_size())


def get_width(surface=None):
    if surface:
        return surface.get_width()
    else:
        return pg.display.get_surface().get_width()


def get_height(surface=None):
    if surface:
        return surface.get_height()
    else:
        return pg.display.get_surface().get_height()


def get_center(surface=None):
    w, h = get_size(surface)
    return Position(w / 2, h / 2)


def get_mouse_pos():
    return Position(pg.mouse.get_pos())

def create_text(text, font, antialias=True, color='white', background=None):
    return font.render(str(text), antialias, color, background)

def draw_text(surface, text, pos, font, antialias=True, color='white', background=None, anchor='tl'):
    txt = create_text(text, font, antialias, color, background)
    rect = txt.get_rect()
    pgt.set_rect_pos(rect, pos, anchor)
    surface.blit(txt, rect)
