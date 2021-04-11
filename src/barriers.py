"""
Module, containing different static barriers for a game.
"""
import typing
import pygame as pg

import config


class Ground(pg.sprite.Sprite):
    """
    Class representing ground segment.

    :param images_holder: dictionary with loaded sprite images
    :param x_position: x-position of of new ground segment
    :param y_position: y-position of of new ground segment
    :param width: Width of new ground segment
    """

    def __init__(self,
                 images_holder: typing.Dict[str, pg.Surface],
                 x_position: int,
                 y_position: int,
                 width: int) -> None:
        """Create new ground segment."""
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((width, config.BRICK_SIZE * 2), pg.SRCALPHA).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position
        grass = images_holder['grass']
        grass = pg.transform.scale(grass, (config.BRICK_SIZE, config.BRICK_SIZE))
        ground = images_holder['ground']
        ground = pg.transform.scale(ground, (config.BRICK_SIZE, config.BRICK_SIZE))
        for x_pos in range(0, width, config.BRICK_SIZE):
            self.image.blit(grass, (x_pos, 0))
        for x_pos in range(0, width, config.BRICK_SIZE):
            self.image.blit(ground, (x_pos, config.BRICK_SIZE))


class BrickBarrier(pg.sprite.Sprite):
    """
    Class representing some barrier.

    :param x_position: x-position of of new ground segment
    :param y_position: y-position of of new ground segment
    :param image: Image of this barrier
    """

    def __init__(self, x_position: int, y_position: int, image: pg.Surface) -> None:
        pg.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x_position
        self.rect.y = y_position
