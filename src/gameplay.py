"""Module, containing gamplay controlling class."""
import os
import typing
import pygame as pg

import level


class Gameplay:
    """
    Class for controlling of gamplay.

    :param level: Current level of gameplay
    :param screen: Surface with whole screen
    """

    def __init__(self, cur_level: level.BasicLevel, screen: pg.Surface) -> None:
        """Create gameplay object."""
        self.images_holder = self.load_all_images("./images")
        self.cur_level = cur_level
        self.screen = screen
        self.clock = pg.time.Clock()
        self.old_time = pg.time.get_ticks()
        self.fps = 60
        self.finished = False
        self.keys_pressed = pg.key.get_pressed()

    @staticmethod
    def load_all_images(directory: str) -> typing.Dict[str, pg.Surface]:
        """
        Load all images from directory.

        :param directory: Path to a directory with sprites and images
        """
        images = {}
        for pic in os.listdir(directory):
            name, ext = os.path.splitext(pic)
            if ext.lower() == '.png':
                img = pg.image.load(os.path.join(directory, pic))
                img = img.convert_alpha()
                images[name] = img
        return images

    def mainloop(self) -> None:
        """Game main loop."""
        self.cur_level.start_level(self.images_holder, self.screen)
        while not self.finished:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.finished = True
                self.keys_pressed = pg.key.get_pressed()
            new_time = pg.time.get_ticks()
            self.cur_level.update(self.keys_pressed, (new_time - self.old_time) / 1000.0)
            self.old_time = new_time
            pg.display.update()
            self.clock.tick(self.fps)
            if self.cur_level.finished:
                self.finished = True
