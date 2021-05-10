"""Module, containing implementaion of dog enemy."""
import typing

import pygame as pg
from . import moving_object
from . import config


class Dog(moving_object.BaseMovingObject):
    """
    Class for dog enemy.

    :param images_holder: dictionary with loaded sprite images
    :param x_position: x-position of a dog
    :param y_position: y-position of a dog
    :param min_left_position: minimum left barrirer for left position of a dog
    :param max_right_position: maximum right for left position of a dog
    :param start_direction: start direction of moving dog
    :param speed: speed of a dog
    """

    def __init__(self, images_holder: typing.Dict[str, pg.Surface],
                 x_position: int,
                 y_position: int,
                 min_left_position: int,
                 max_right_position: int,
                 start_direction: int,
                 speed: int) -> None:
        """Create dog enemy and initialize state variables."""
        size = (config.BRICK_SIZE, config.BRICK_SIZE)
        super().__init__(size)
        self.sprites = moving_object.generate_rotated_images(images_holder['dog'], size)
        self.image = self.sprites['right_direction']
        self.update_sprite_view()
        self.x_position = x_position
        self.y_position = y_position
        self.min_left_position = min_left_position
        self.max_right_position = max_right_position
        self.start_direction = start_direction
        self.speed = speed

    def update_speed(self, diff_time: float) -> None:
        """
        Update speed of a dog depending on passed time after last call.

        :param diff_time: Amount of time passed after last call
        """
        if self.state == 'stand' or self.state == 'walk':
            self.state = 'walk'
            if self.x_speed == 0:
                self.x_speed = self.speed * self.start_direction
                self.x_position += self.start_direction
                self.start_direction *= -1
        elif self.state == 'fall':
            self.update_falling_speed(diff_time)

    def update_falling_speed(self, diff_time: float) -> None:
        """
        Update speed of a falling dog depending on passed time after last call.

        :param diff_time: Amount of time passed after last call
        """
        self.y_speed += config.GRAVITY * diff_time
        self.y_speed = min(self.y_speed, config.CAT_MAX_Y_SPEED)

    def update_position(self,
                        all_barriers_group: pg.sprite.Group,
                        diff_time: float,
                        cat_rect: pg.Rect) -> typing.List[pg.sprite.Sprite]:
        """
        Update dog position depending on objects around him, and by passed time after last call.

        :param all_barriers_group: Objects around dog
        :param diff_time: Amount of time passed after last call
        :param cat_rect: Rectangle of a cat for checking if it killed dog
        """
        if self.state == 'dying':
            self.update_dying_view(diff_time)
            return []
        self.update_sprite_view()
        before_top = self.rect.top
        collides = []
        self.x_position += self.x_speed * diff_time
        self.y_position += self.y_speed * diff_time
        if self.x_position <= self.min_left_position or self.x_position >= self.max_right_position:
            self.x_speed = 0
            self.x_position = min(self.max_right_position, max(self.x_position, self.min_left_position))
        self.rect.x = int(self.x_position)
        collides.append(self.manage_x_collisions(all_barriers_group))
        self.rect.y = int(self.y_position)
        collides.append(self.manage_y_collisions(all_barriers_group))
        self.detect_falling(all_barriers_group)

        for collide in collides:
            if collide is not None and collide.rect == cat_rect and cat_rect.bottom <= before_top + 10:
                self.start_dying()
        return collides

    def start_dying(self) -> None:
        """Start dog dying animation."""
        self.state = 'dying'
        self.x_speed = 0
        self.y_speed = 0
        self.x_acceleration = 0
        self.dying_shrink = 0

    def update_dying_view(self, diff_time: float) -> None:
        """Update dog dying animation.

        :param diff_time: Amount of time passed after last call
        """
        self.dying_shrink += 20.0 * diff_time
        self.rect.y = self.y_position + self.dying_shrink
        self.image = pg.transform.smoothscale(self.image, (self.rect.width, int(config.BRICK_SIZE - self.dying_shrink)))
        if self.dying_shrink >= config.BRICK_SIZE:
            self.is_killed = True
