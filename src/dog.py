"""
Module, containing implementaion of dog enemy.
"""
import typing

import pygame as pg
import moving_object
import config


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
        super().__init__()
        self.sprite = images_holder['dog']
        self.image = pg.transform.scale(self.sprite, (40, 40))
        self.rect = self.image.get_rect()
        self.x_position = x_position
        self.y_position = y_position
        self.min_left_position = min_left_position
        self.max_right_position = max_right_position
        self.start_direction = start_direction
        self.speed = speed

    def update_speed(self, diff_time: float) -> None:
        """
        Update speed of a dog depending 
        on passed time after last call.

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
        Update speed of a falling dog depending
        on passed time after last call.

        :param diff_time: Amount of time passed after last call
        """
        self.y_speed += config.GRAVITY * diff_time
        self.y_speed = min(self.y_speed, config.CAT_MAX_Y_SPEED)

    def update_position(self,
                        all_barriers_group: pg.sprite.Group,
                        diff_time: float,
                        cat_rect: pg.Rect) -> typing.List[pg.sprite.Sprite]:
        """
        Update dog position depending on objects around him,
        and by passed time after last call.

        :param all_barriers_group: Objects around dog
        :param diff_time: Amount of time passed after last call
        :param cat_rect: Rectangle of a cat for checking if it killed dog
        """
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
            if collide is not None and collide.rect == cat_rect and cat_rect.bottom <= before_top + 2:
                self.is_killed = True
        return collides
