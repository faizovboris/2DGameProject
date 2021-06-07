"""Module, containing gameplay controlling class."""
import os
import typing
import pygame as pg

from . import level
from . import counter


class Gameplay:
    """
    Class for controlling of gameplay.

    :param cur_level: Current level of gameplay
    :param screen: Surface with whole screen
    :param images_dir: Path to folder with images
    """

    def __init__(self, levels: typing.List[level.BasicLevel], screen: pg.Surface,
                 images_dir: str, counter: counter.Counter) -> None:
        """Create gameplay object."""
        self.images_holder = self.load_all_images(images_dir)
        self.counter = counter
        self.all_levels = levels
        self.cur_level = 0
        self.screen = screen
        self.clock = pg.time.Clock()
        self.old_time = pg.time.get_ticks()
        self.fps = 60
        self.finished = False
        self.quit_pressed = False
        self.keys_pressed = pg.key.get_pressed()
        self.win = False

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
        level = self.all_levels[self.cur_level]
        level.start_level(self.images_holder, self.screen)
        while self.cur_level < len(self.all_levels) and not self.quit_pressed:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.finished = True
                    self.quit_pressed = True
                self.keys_pressed = pg.key.get_pressed()
            new_time = pg.time.get_ticks()
            level.update(self.keys_pressed, (new_time - self.old_time) / 1000.0)
            self.old_time = new_time
            pg.display.update()
            self.clock.tick(self.fps)
            if level.finished:
                if level.win:
                    self.counter.max_position = 0
                    self.cur_level += 1
                    if self.cur_level >= len(self.all_levels):
                        self.win = True
                        break
                    level = self.all_levels[self.cur_level]
                    level.start_level(self.images_holder, self.screen)
                elif self.counter.get_lives() == 1:
                    break
                else:
                    self.counter.miss_life()
                    level = self.all_levels[self.cur_level]
                    level.start_level(self.images_holder, self.screen)
