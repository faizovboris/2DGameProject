"""
Module, containing implementaion of basic moving object.
"""
import typing

import pygame as pg
import config


class BaseMovingObject(pg.sprite.Sprite):
    """
    Base class for movinf object.
    """

    def __init__(self) -> None:
        """Create moving object and initialize state variables."""
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 10)).convert()
        self.rect = self.image.get_rect()
        self.state = 'stand'
        self.x_position = 0
        self.y_position = 0
        self.x_speed = 0
        self.y_speed = 0
        self.x_acceleration = 0
        self.is_killed = False

    def update_speed(self) -> None:
        """Update speed of an object"""
        pass

    def update_position(self):
        """Update position of an object"""
        pass

    def manage_x_collisions(self, all_barriers_group: pg.sprite.Group) -> pg.sprite.Sprite:
        """
        Manage and resolve horisontal object collisions with environment.

        :param all_barriers_group: Barriers around object
        """
        collider = pg.sprite.spritecollideany(self, all_barriers_group)
        if collider:
            if self.rect.x < collider.rect.x:
                self.rect.right = collider.rect.left
            else:
                self.rect.left = collider.rect.right
            self.x_speed = 0
            self.x_position = self.rect.x
        return collider

    def manage_y_collisions(self, all_barriers_group: pg.sprite.Group) -> pg.sprite.Sprite:
        """
        Manage and resolve vertical object collisions with environment.

        :param all_barriers_group: Barriers around object
        """
        collider = pg.sprite.spritecollideany(self, all_barriers_group)
        if collider:
            if collider.rect.bottom > self.rect.bottom:
                self.rect.bottom = collider.rect.top
                self.state = 'walk'
            else:
                self.rect.top = collider.rect.bottom
                self.state = 'fall'
            self.y_speed = 0
            self.y_position = self.rect.y
        else:
            collider = None
        return collider

    def detect_falling(self, all_barriers_group: pg.sprite.Group) -> None:
        """
        Check if object started falling.

        :param all_barriers_group: Barriers around moving object
        """
        self.rect.y += 1
        collider = pg.sprite.spritecollideany(self, all_barriers_group)
        if collider is None and self.state != 'jump':
            self.state = 'fall'
        self.rect.y -= 1

    def update_sprite_view(self) -> None:
        """Update sprite depending on move direction."""
        if self.x_speed >= -5:
            self.image = self.sprites['right_direction']
        else:
            self.image = self.sprites['left_direction']
        bottom, left = self.rect.bottom, self.rect.x
        self.rect = self.image.get_rect()
        self.rect.bottom, self.rect.x = bottom, left


def generate_rotated_images(image, size):
    """
    Generate images rotated for different moving directions.

    :param size: Desired sprite size
    """
    image = pg.transform.scale(image, size)
    return {
        'right_direction': image,
        'left_direction': pg.transform.flip(image, True, False)
    }
