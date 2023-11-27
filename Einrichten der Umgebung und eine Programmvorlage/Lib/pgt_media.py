import pygame as pg
from pygame.locals import *
import pygame.sprite as sprite
import os
import math
import random
import pathlib
import pgtools as pgt



class Media:
    media_dir = "media"
    soundvolume = 1
    sounds = {}

    @classmethod
    def set_soundvolume(cls, volume):
        cls.soundvolume = volume

    @classmethod
    def load_sound(cls, name, filename):
        fullname = os.path.join(cls.media_dir, filename)
        cls.sounds[name] = pg.mixer.Sound(fullname)

    @classmethod
    def play_sound(cls, name, volume=None):
        if not volume: volume = cls.soundvolume
        cls.sounds[name].set_volume(volume)
        pg.mixer.Sound.play(cls.sounds[name])

    @classmethod
    def play_music(cls, filename,):
        fullname = os.path.join(cls.media_dir, filename)
        pg.mixer.music.load(fullname)
        pg.mixer.music.play(-1)

    @classmethod
    def set_volume(cls, volume):
        pg.mixer.music.set_volume(volume)

    @classmethod
    def stop_music(cls):
        pg.mixer.music.stop()

    @classmethod
    def pause_music(cls):
        pg.mixer.music.pause()

    @classmethod
    def unpause_music(cls):
        pg.mixer.music.unpause()

    @classmethod
    def load_image(cls, filename, size=None, width=None, height=None, colorkey=None, createfullname=True):
        if createfullname:
            fullname = os.path.join(cls.media_dir, filename)
        else:
            fullname = filename
        try:
            image = pg.image.load(fullname)
            if width and height:
                size = pgt.Size(width, height)
            elif width:
                sz = image.get_size()
                f = sz[1] / sz[0]
                height = width * f
                size = pgt.Size(width, height)
            elif height:
                sz = image.get_size()
                f = sz[0] / sz[1]
                width = height * f
                size = pgt.Size(width, height)
            if size:
                image = pg.transform.scale(image, size)

            if colorkey is not None:
                image = image.convert()
                if colorkey == -1:
                    colorkey = image.get_at((0, 0))
                image.set_colorkey(colorkey, pg.RLEACCEL)
            elif image.get_alpha() is None:
                image = image.convert()
            else:
                image = image.convert_alpha()
        except FileNotFoundError:
            print(f"{fullname} kann nicht geladen werden.")
            raise SystemExit
        return image

    @classmethod
    def load_images(cls, filename, size=None, width=None, height=None, colorkey=None):
        fullname = os.path.join(cls.media_dir, filename)
        files = [f for f in pathlib.Path().glob(fullname)]
        files.sort()
        images = []
        for name in files:
            images.append(cls.load_image(name, size, width, height, colorkey, createfullname=False))
        return images
