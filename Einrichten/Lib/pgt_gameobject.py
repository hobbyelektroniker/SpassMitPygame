import pygame as pg
from pygame.locals import *
import pygame.sprite as sprite
import os
import math
import random
import pathlib
from pttools import *
import pgtools as pgt
from pgt_gameclass import Game, Function



class SpriteObject(pg.sprite.Sprite):
    def __init__(self, game, *, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True,
                 tcolor=(0, 0, 0), group=None):
        super().__init__()
        self.game = game
        self.tcolor = tcolor
        self.size = pgt.Size(size)
        self._anchor = anchor
        self.done = False
        self.handleevents = False
        self.vars = []
        self.functions = []
        self.hit_left = self.hit_right = self.hit_top = self.hit_bottom = 0

        self.image = pg.Surface(size)
        if tcolor:
            self.image.set_colorkey(tcolor)
        self.image.convert()
        if tcolor:
            self.image.fill(tcolor)

        self.rect = self.image.get_rect()
        pgt.set_rect_pos(self.rect, pos, anchor=anchor)
        if active:
            self.add(game.update_sprites)
        if visible:
            self.add(game.visible_sprites)
        if group is not None:
            self.add(group)

    def shrink_box(self, left=None, right=None, top=None, bottom=None):
        if left is not None: self.hit_left = left
        if right is not None: self.hit_right = right
        if top is not None: self.hit_top = top
        if bottom is not None: self.hit_bottom = bottom

    def activate_events(self, value=True):
        if value and not self.handleevents:
            self.handleevents = True
            v = self.add_var(self.game.app_event)
            v.trace_add(self._handle_event, 'w')
        elif not value and self.handleevents:
            self.handleevents = False
            self.remove_var(self.game.app_event)


    def add_var(self, var):
        self.vars.append(var)
        return var

    def remove_var(self, var):
        if var in self.vars:
            self.vars.remove(var)

    def __del__(self):
        for v in self.vars:
            v.trace_clear()
        self.vars.clear()


    def hitbox(self):
        box = self.rect.copy()
        box.x += self.hit_left
        box.width -= (self.hit_left + self.hit_right)
        box.y += self.hit_top
        box.height -= (self.hit_top + self.hit_bottom)
        return box

    def collide_with_group(self, group, dokill=False):
        return sprite.spritecollide(self, group, dokill=dokill, collided=pgt.hitbox_collide)

    def _handle_event(self, *args):
        event = self.game.app_event.value
        if event:
            self.handle_event(event)

    def handle_event(self, event):
        pass

    def function(self, seconds, func, *, loops=0, **kwargs):
        t = Function(seconds, func, loops=loops, **kwargs)
        self.functions.append(t)
        return t

    def after(self, seconds, func, **kwargs):
        self.function(seconds, func, loops=1, **kwargs)

    def run_tasks(self):
        for task in self.functions:
            task.execute()
        self.functions = [task for task in self.functions if not task.done]

    def update(self, dt):
        super().update()
        self.run_tasks()

    def set_anchor(self, anchor):
        # rect wird umgerechnet, pos bleibt erhalten
        if anchor != self.anchor:
            pos = pgt.get_rect_pos(self.rect, self.anchor)  # alte Ankerposition
            self._anchor = anchor
            pgt.set_rect_pos(self.rect, pos, self.anchor)  # neuer Anker kommt an die alte Ankerposition

    def change_anchor(self, anchor):
        # rect bleibt an Position, pos wird umgerechnet
        if anchor != self.anchor:
            self._anchor = anchor

    def set_pos(self, pos):
        pgt.set_rect_pos(self.rect, pos, self.anchor)

    @property
    def pos(self):
        return pgt.get_rect_pos(self.rect, self.anchor)

    @pos.setter
    def pos(self, value):
        pgt.set_rect_pos(self.rect, value, self.anchor)

    @property
    def anchor(self):
        return self._anchor

    @anchor.setter
    def anchor(self, value):
        self.set_anchor(value)

    @property
    def visible(self):
        return self in self.game.visible_sprites

    @visible.setter
    def visible(self, value):
        if value and not self.visible:
            self.add(self.game.visible_sprites)
        elif not value and self.visible:
            self.remove(self.game.visible_sprites)

    @property
    def active(self):
        return self in self.game.update_sprites

    @active.setter
    def active(self, value):
        if value and not self.active:
            self.add(self.game.update_sprites)
        elif not value and self.visible:
            self.remove(self.game.update_sprites)

class GameObject(SpriteObject):
    def __init__(self, game, *, pos=(0, 0), size=(50, 50), anchor='tl', active=True, visible=True,
                 tcolor=(0, 0, 0), group=None):
        super().__init__(game=game, pos=pos, size=size, anchor=anchor, active=active, visible=visible, tcolor=tcolor,
                         group=group)
        self._collidable = False
        self.speed = 0
        self.direction = pgt.Direction()
        self._keyboard_move = None
        self._constraints = None
        self.done = False

        # .add(*groups), .remove(*groups), .kill(), .'alive()

    def set_image(self, image):
        pos = self.pos
        self.image = image
        self.rect = self.image.get_rect()
        self.size = self.rect.size
        self.pos = pos


    def update(self, dt):
        super().update(dt)
        if self._keyboard_move:
            keys = pg.key.get_pressed()
            auf, ab, links, rechts = self._keyboard_move
            if auf and keys[auf]:
                self.direction.y = -1
            elif ab and keys[ab]:
                self.direction.y = 1
            elif auf or ab:
                self.direction.y = 0
            if links and keys[links]:
                self.direction.x = -1
            elif rechts and keys[rechts]:
                self.direction.x = 1
            elif links or rechts:
                self.direction.x = 0
            if self.direction.length():
                self.direction.normalize_ip()

        if self.speed and len(self.direction):
            self.rect.topleft += pgt.pixels_to_move(self.direction, self.speed, dt)

        if self._constraints:
            oben, unten, links, rechts = self._constraints
            if oben is not None and oben > self.rect.top:
                self.rect.top = oben
            elif unten is not None and unten < self.rect.bottom:
                self.rect.bottom = unten
            if links is not None and links > self.rect.left:
                self.rect.left = links
            elif rechts is not None and rechts < self.rect.right:
                self.rect.right = rechts

    def keyboard_move(self, *, up=None, down=None, left=None, right=None):
        self._keyboard_move = (up, down, left, right)

    def constraints(self, top=None, bottom=None, left=None, right=None):
        self._constraints = (top, bottom, left, right)


class AnimatedGameObject(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.image_idx = 0
        self.tm = 0
        self.animating = False
        self.image = None
        self.image_list = []
        self.dtm = 0
        self.fps = 10

    @property
    def fps(self):
        return self._fps

    @fps.setter
    def fps(self, value):
        self._fps = value
        if value:
            self.dtm = 1000 / value
        else:
            self.animating = False

    def load_animation(self, filename, fps=10, **kwargs):
        self.fps = fps
        self.image_list = pgt.Media.load_images(filename, **kwargs)
        self.image = self.image_list[0]

    def update(self, dt):
        if self.animating and self.tm <= pg.time.get_ticks():
            self.image_idx += 1
            if self.image_idx >= len(self.image_list):
                self.image_idx = 0
            self.set_image(self.image_list[self.image_idx])
            self.tm = pg.time.get_ticks() + self.dtm
        super().update(dt)

    def animate(self, value=True):
        if value:
            self.tm = pg.time.get_ticks() + self.dtm
            self.animating = True
            self.image_idx = 0
        else:
            self.animating = False

