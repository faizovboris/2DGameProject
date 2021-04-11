"""
Module, containing implementaion player cat.
"""
import typing

import pygame as pg
import moving_object
import config


class Cat(moving_object.BaseMovingObject):
    """
    Class for cat player object.

    :param images_holder: dictionary with loaded sprite images
    """

    def __init__(self, images_holder: typing.Dict[str, pg.Surface]) -> None:
        """Create cat object and initialize state variables."""
        super().__init__()
        self.sprite = images_holder['cat']
        self.image = pg.transform.scale(self.sprite, (40, 40))
        self.rect = self.image.get_rect()

    def update_speed(self, keys: pg.key.ScancodeWrapper, diff_time: float) -> None:
        """
        Update speed of a cat depending in pressed by
        player buttons and on passed time after last call.

        :param keys: Contains pressed by user buttons
        :param diff_time: Amount of time passed after last call
        """
        if self.state == 'stand':
            self.update_standing_speed(keys, diff_time)
        elif self.state == 'walk':
            self.update_walking_speed(keys, diff_time)
        elif self.state == 'jump':
            self.update_jumping_speed(keys, diff_time)
        elif self.state == 'fall':
            self.update_falling_speed(keys, diff_time)
        self.update_x_speed(keys, diff_time)
        self.x_speed = max(-config.CAT_MAX_X_SPEED, min(config.CAT_MAX_X_SPEED, self.x_speed))
        self.y_speed = min(self.y_speed, config.CAT_MAX_Y_SPEED)

    def update_standing_speed(self, keys: pg.key.ScancodeWrapper, diff_time: float) -> None:
        """
        Update speed of a standing cat depending in pressed by
        player buttons and on passed time after last call.

        :param keys: Contains pressed by user buttons
        :param diff_time: Amount of time passed after last call
        """
        self.x_speed = 0
        self.y_speed = 0
        self.state = 'stand'
        if keys[pg.K_LEFT] or keys[pg.K_RIGHT]:
            self.state = 'walk'
        elif keys[pg.K_UP]:
            self.state = 'jump'
            self.y_speed = config.CAT_JUMP_SPEED

    def update_walking_speed(self, keys: pg.key.ScancodeWrapper, diff_time: float) -> None:
        """
        Update speed of a walking cat depending in pressed by
        player buttons and on passed time after last call.

        :param keys: Contains pressed by user buttons
        :param diff_time: Amount of time passed after last call
        """
        if keys[pg.K_UP]:
            self.state = 'jump'
            self.y_speed = config.CAT_JUMP_SPEED

    def update_jumping_speed(self, keys: pg.key.ScancodeWrapper, diff_time: float) -> None:
        """
        Update speed of a jumping cat depending in pressed by
        player buttons and on passed time after last call.

        :param keys: Contains pressed by user buttons
        :param diff_time: Amount of time passed after last call
        """
        self.y_speed += config.JUMP_GRAVITY * diff_time
        if self.y_speed >= 0 or not keys[pg.K_UP]:
            self.state = 'fall'

    def update_falling_speed(self, keys: pg.key.ScancodeWrapper, diff_time: float) -> None:
        """
        Update speed of a falling cat depending in pressed by
        player buttons and on passed time after last call.

        :param keys: Contains pressed by user buttons
        :param diff_time: Amount of time passed after last call
        """
        self.y_speed += config.GRAVITY * diff_time

    def update_x_speed(self, keys: pg.key.ScancodeWrapper, diff_time: float) -> None:
        """
        Update horisontal speed of a cat depending on pressed by
        player buttons and on passed time after last call.

        :param keys: Contains pressed by user buttons
        :param diff_time: Amount of time passed after last call
        """
        self.x_acceleration = config.CAT_WALK_ACCELERATION * \
            (-1 if self.x_speed > 0 else 1 if self.x_speed < 0 else 0)
        if keys[pg.K_LEFT]:
            if self.x_speed > 0:
                self.x_acceleration = -config.CAT_CHANGE_DIRECTION_ACCELERATION
            else:
                self.x_acceleration = -config.CAT_WALK_ACCELERATION
        elif keys[pg.K_RIGHT]:
            if self.x_speed < 0:
                self.x_acceleration = config.CAT_CHANGE_DIRECTION_ACCELERATION
            else:
                self.x_acceleration = config.CAT_WALK_ACCELERATION
        self.x_speed += self.x_acceleration * diff_time
        if self.x_speed == 0 and self.state == 'walk':
            self.state = 'stand'

    def update_position(self,
                        all_barriers_group: pg.sprite.Group,
                        min_x_pos: int,
                        diff_time: float) -> typing.List[pg.sprite.Sprite]:
        """
        Update cat position depending on barriers around him,
        minimum possible position due to environment and by
        passed time after last call.

        :param all_barriers_group: Barriers around cat
        :param min_x_pos: Minimum possible horisontal position due to environment and view rectangle
        :param diff_time: Amount of time passed after last call
        """
        collides = []
        self.x_position += self.x_speed * diff_time
        self.y_position += self.y_speed * diff_time
        self.rect.x = int(self.x_position)
        collides.append(self.manage_x_collisions(all_barriers_group))
        self.rect.y = int(self.y_position)
        collides.append(self.manage_y_collisions(all_barriers_group))
        self.detect_falling(all_barriers_group)
        self.rect.x = max(self.rect.x, min_x_pos)
        return collides
