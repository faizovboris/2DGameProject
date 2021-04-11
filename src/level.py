"""
Module, containing implementaion of game levels.
"""
import typing
import pygame as pg

import config
import barriers
import cat
import dog


class BasicLevel:
    """Basic level class."""

    def __init__(self) -> None:
        """Create BasicLevel object."""
        pass


class Level(BasicLevel):
    """Class with gameplay of simple level."""

    def __init__(self) -> None:
        """Create this level object."""
        self.finished = False
        super().__init__()

    def start_level(self, images_holder: typing.Dict[str, pg.Surface], screen: pg.Surface) -> None:
        """
        Start new level.

        :param images_holder: All images and sprites
        :param screen: Surface with whole screen
        """
        self.images_holder = images_holder
        self.screen = screen
        self.init_background()
        self.init_ground()
        self.init_barriers()
        self.init_dogs()
        self.init_cat()
        self.static_barriers_group = pg.sprite.Group(self.ground_group, self.barrier_group)
        self.all_elements_group = pg.sprite.Group(self.static_barriers_group,
                                                  self.cat_group,
                                                  self.dogs_group)

    def init_background(self) -> None:
        """Initialize background objects of this level."""
        width, height = 9000, 600
        self.background = pg.Surface((width, height)).convert()
        self.background.fill(config.SKY_COLOR)
        self.level = pg.Surface((width, height)).convert()
        self.level_rect = self.level.get_rect()
        self.view = self.screen.get_rect(bottom=self.level_rect.bottom)

    def init_ground(self) -> None:
        """Initialize ground for this level."""
        GROUND_POSITIONS_INFO = [
            (0, config.GROUND_Y_POSITION, 1001),  # x, y, width
            (1060, config.GROUND_Y_POSITION, 1001),  # x, y, width
        ]
        ground_segments = []
        for position in GROUND_POSITIONS_INFO:
            new_ground_segment = barriers.Ground(self.images_holder, position[0], position[1], position[2])
            ground_segments.append(new_ground_segment)
            self.background.blit(new_ground_segment.image, (position[0], position[1]))
        self.ground_group = pg.sprite.Group(* ground_segments)

    def init_barriers(self) -> None:
        """Initialize ground barriers for this level."""
        BARRIER_POSITIONS_INFO = [
            (200, config.GROUND_Y_POSITION - config.BRICK_SIZE),
            (240, config.GROUND_Y_POSITION - config.BRICK_SIZE),
            (240, config.GROUND_Y_POSITION - 2 * config.BRICK_SIZE),
            (600, config.GROUND_Y_POSITION - 4 * config.BRICK_SIZE),
            (640, config.GROUND_Y_POSITION - 4 * config.BRICK_SIZE),
            (680, config.GROUND_Y_POSITION - 4 * config.BRICK_SIZE),
        ]
        barrier_brick_image = self.images_holder['brick']
        barrier_brick_image = pg.transform.scale(barrier_brick_image, (config.BRICK_SIZE, config.BRICK_SIZE))
        barrier_colliders = []
        for position in BARRIER_POSITIONS_INFO:
            new_brick = barriers.BrickBarrier(position[0], position[1], barrier_brick_image)
            barrier_colliders.append(new_brick)
            self.background.blit(new_brick.image, (position[0], position[1]))
        self.barrier_group = pg.sprite.Group(* barrier_colliders)
    
    def init_dogs(self) -> None:
        """Initialize dogs for this level."""
        DOGS_POSITIONS_INFO = [
            (640, config.GROUND_Y_POSITION - 5 * config.BRICK_SIZE, 300, 800, 1, 50),  # x, y, min_x, max_x, start_direction, speed
        ]
        self.dogs = []
        for position in DOGS_POSITIONS_INFO:
            new_dog = dog.Dog(self.images_holder, position[0], position[1], position[2], position[3], position[4], position[5])
            self.dogs.append(new_dog)
        self.dogs_group = pg.sprite.Group(* self.dogs)

    def init_cat(self) -> None:
        """Initialize cat for this level."""
        self.cat = cat.Cat(self.images_holder)
        self.cat.x_position = 5
        self.cat.y_position = config.GROUND_Y_POSITION
        self.cat_group = pg.sprite.Group(self.cat)

    def update(self, keys: pg.key.ScancodeWrapper, diff_time: float) -> None:
        """
        Update level after next time tick.

        :param keys: Contains pressed by user buttons
        :param diff_time: Amount of time passed after last call
        """
        self.cat.update_speed(keys, diff_time)
        self.cat.update_position(self.static_barriers_group, self.view.x + 5, diff_time)
        self.update_dogs(diff_time)
        self.update_view()
        self.draw_scene()
        if self.cat.is_killed:
            self.finished = True
    
    def update_dogs(self, diff_time) -> None:
        """
        Update dogs after next time tick.

        :param diff_time: Amount of time passed after last call
        """
        for i, dog in enumerate(self.dogs):
            dog.kill()
            dog.update_speed(diff_time)
            dog_collides = dog.update_position(self.all_elements_group, diff_time, self.cat.rect)
            for collide in dog_collides:
                if collide == self.cat and not dog.is_killed:
                    self.cat.is_killed = True
            if dog.is_killed:
                del self.dogs[i]
            else:
                self.dogs_group.add(dog)
                self.all_elements_group.add(dog)

    def update_view(self) -> None:
        """Update view position after next time tick."""
        max_not_moving_position = self.view.x + 2 * self.view.w // 3
        need_move = max(0, self.cat.rect.centerx - max_not_moving_position)
        rightmost_position = self.level_rect.w - self.view.w
        self.view.x = min(rightmost_position, self.view.x + need_move)

    def draw_scene(self) -> None:
        """Draw updated scene."""
        self.level.blit(self.background, self.view, self.view)
        self.cat_group.draw(self.level)
        self.dogs_group.draw(self.level)
        self.screen.blit(self.level, (0, 0), self.view)
