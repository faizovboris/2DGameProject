"""Module, containing implementaion of game levels."""
import os
import csv
import typing
import pygame as pg

from . import config
from . import barriers
from . import cat
from . import dog
from . import sound_manager


class BasicLevel:
    """Basic level class."""

    def __init__(self) -> None:
        """Create BasicLevel object."""
        pass


class Level(BasicLevel):
    """Class with gameplay of simple level.

    :param directory: Directory with info about objects in level
    """

    def __init__(self, directory: str, sounds: sound_manager.SoundManager) -> None:
        """Create this level object."""
        self.sounds = sounds
        self.finished = False
        self.win = False
        super().__init__()
        self.level_info = parse_level_info(directory)

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
        width, height = config.MAX_LEVEL_WIDTH, config.SCREEN_HEIGHT
        self.background = pg.Surface((width, height)).convert()
        self.background.fill(config.SKY_COLOR)
        self.level = pg.Surface((width, height)).convert()
        self.level_rect = self.level.get_rect()
        self.view = self.screen.get_rect(bottom=self.level_rect.bottom)

    def init_ground(self) -> None:
        """Initialize ground for this level."""
        ground_positions_info = self.level_info['ground']
        ground_segments = []
        for cur_position_info in ground_positions_info:
            x_position = int(cur_position_info['x'])
            y_position = config.GROUND_Y_POSITION - int(cur_position_info['y'])
            width = int(cur_position_info['width'])
            new_ground_segment = barriers.Ground(self.images_holder,
                                                 x_position=x_position,
                                                 y_position=y_position,
                                                 width=width)
            ground_segments.append(new_ground_segment)
            self.background.blit(new_ground_segment.image, (x_position, y_position))
        self.ground_group = pg.sprite.Group(* ground_segments)

    def init_barriers(self) -> None:
        """Initialize ground barriers for this level."""
        barrier_positions_info = self.level_info['barriers']
        barrier_colliders = []
        for cur_position_info in barrier_positions_info:
            x_position = int(cur_position_info['x'])
            y_position = config.GROUND_Y_POSITION - int(cur_position_info['y'])
            barrier_brick_image = self.images_holder[cur_position_info['sprite']]
            barrier_brick_image = pg.transform.scale(barrier_brick_image, (config.BRICK_SIZE, config.BRICK_SIZE))
            new_brick = barriers.BrickBarrier(x_position=x_position,
                                              y_position=y_position,
                                              image=barrier_brick_image)
            barrier_colliders.append(new_brick)
            self.background.blit(new_brick.image, (x_position, y_position))
        self.barrier_group = pg.sprite.Group(* barrier_colliders)

    def init_dogs(self) -> None:
        """Initialize dogs for this level."""
        dogs_positions_info = self.level_info['dogs']
        self.dogs = []
        for cur_position_info in dogs_positions_info:
            new_dog = dog.Dog(self.images_holder,
                              x_position=int(cur_position_info['x']),
                              y_position=config.GROUND_Y_POSITION - int(cur_position_info['y']),
                              min_left_position=int(cur_position_info['min_x']),
                              max_right_position=int(cur_position_info['max_x']),
                              start_direction=int(cur_position_info['start_direction']),
                              speed=int(cur_position_info['speed']))
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
        if self.cat.state == 'fall' and self.cat.y_position >= config.SCREEN_HEIGHT:
            self.cat.is_killed = True
        self.update_dogs(diff_time)
        self.update_view()
        self.draw_scene()
        if self.cat.x_position >= config.MAX_LEVEL_WIDTH - 100:
            self.win = True
            self.finished = True
        if self.cat.is_killed:
            self.finished = True
            self.win = False

    def update_dogs(self, diff_time) -> None:
        """
        Update dogs after next time tick.

        :param diff_time: Amount of time passed after last call
        """
        for i, dog_instance in enumerate(self.dogs):
            dog_instance.kill()
            dog_instance.update_speed(diff_time)
            dog_collides = dog_instance.update_position(self.all_elements_group, diff_time, self.cat.rect)
            for collide in dog_collides:
                if collide == self.cat:
                    if dog_instance.is_killed or dog_instance.state == 'dying':
                        self.cat.y_speed += config.CAT_ENEMY_KILLING_JUMP_SPEED
                        self.cat.state = 'jump'
                        self.sounds.set_effect('kill_dog')
                    else:
                        self.cat.is_killed = True
                        self.sounds.set_effect('kill_cat')
            if dog_instance.state == 'fall' and dog_instance.y_position >= config.SCREEN_HEIGHT:
                dog_instance.is_killed = True
            if dog_instance.is_killed:
                del self.dogs[i]
            else:
                self.dogs_group.add(dog_instance)
                self.all_elements_group.add(dog_instance)

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


def parse_level_info(directory: str) -> typing.Dict[str, typing.Dict[str, str]]:
    """
    Parse info about object placement in level from files in directory.

    :param directory: Directory with info
    """
    level_info = {}
    for filename in os.listdir(directory):
        name, ext = os.path.splitext(filename)
        if ext.lower() == '.csv':
            with open(os.path.join(directory, filename), 'r') as fr:
                level_info[name] = list(csv.DictReader(fr))
    return level_info
