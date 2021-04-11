"""
Module, containing implementaion player cat.
"""
import typing

import pygame as pg
import config


class Cat(pg.sprite.Sprite):
    """
    Class for cat player object.

    :param images_holder: dictionary with loaded sprite images
    """

    def __init__(self, images_holder) -> None:
        """Create cat object and initialize state variables."""
        pg.sprite.Sprite.__init__(self)
        self.sprite = images_holder['cat']
        self.image = pg.transform.scale(self.sprite, (40, 40))
        self.rect = self.image.get_rect()
        self.state = 'walk'
        self.x_position = 0
        self.y_position = 0
        self.x_speed = 0
        self.y_speed = 0
        self.x_acceleration = 0

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

    def manage_x_collisions(self, all_barriers_group: pg.sprite.Group) -> pg.sprite.Sprite:
        """
        Manage and resolve horisontal cat collisions with environment.

        :param all_barriers_group: Barriers around cat
        """
        collider = pg.sprite.spritecollideany(self, all_barriers_group)
        if collider:
            if self.rect.x < collider.rect.x:
                self.rect.right = collider.rect.left
            else:
                self.rect.left = collider.rect.right
            self.x_speed = 0
        return collider

    def manage_y_collisions(self, all_barriers_group: pg.sprite.Group) -> pg.sprite.Sprite:
        """
        Manage and resolve vertical cat collisions with environment.

        :param all_barriers_group: Barriers around cat
        """
        collider = pg.sprite.spritecollideany(self, all_barriers_group)
        if collider and collider.rect.bottom > self.rect.bottom:
            self.rect.bottom = collider.rect.top
            self.y_speed = 0
            self.state = 'walk'
        else:
            collider = None
        return collider

    def detect_falling(self, all_barriers_group: pg.sprite.Group) -> None:
        """
        Check if cat started falling.

        :param all_barriers_group: Barriers around cat
        """
        self.rect.y += 1
        collider = pg.sprite.spritecollideany(self, all_barriers_group)
        if collider is None and self.state != 'jump':
            self.state = 'fall'
        self.rect.y -= 1
