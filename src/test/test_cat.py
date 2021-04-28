import unittest
from cat import Cat
from gameplay import Gameplay
from test.mocks import PgKeyMock
import pygame as pg
import os
import config
from unittest.mock import MagicMock


class TestCatUpdateSpeedParams:
    def __init__(self, keys, diff, cat_init, cat_res):
        self.keys = keys
        self.init = cat_init
        self.res = cat_res
        self.diff = diff


class TestCat(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        pg.init()
        pg.display.set_caption(("Super Cat"))
        screen = pg.display.set_mode(config.SCREEN_SIZE)
        self.images_holder = Gameplay.load_all_images('./images')

    def setUp(self):
        self.cat = Cat(self.images_holder)
        self.cat.x_position = 10
        self.cat.y_position = 5

    def _test_state_and_key(self, param):
        self.cat.state = param.init["state"]
        self.cat.x_speed = param.init.get("x_speed", 0)
        self.cat.y_speed = param.init.get("y_speed", 0)
        self.cat.update_speed(param.keys, param.diff)
        self.assertEqual(self.cat.state, param.res["state"])
        # position doesn't change
        self.assertEqual(self.cat.x_position, 10)
        self.assertEqual(self.cat.y_position, 5)
        self.assertEqual(self.cat.x_speed, param.res.get("x_speed", 0))
        self.assertEqual(self.cat.y_speed, param.res.get("y_speed", 0))

    def test_speed_stand_update(self):
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.DOWN), 3,
            {"state": "stand"},
            {"state": "stand"}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.UP), 3,
            {"state": "stand"},
            {"state": 'jump',
             "y_speed": config.CAT_JUMP_SPEED}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.RIGHT), 3,
            {"state": "stand"},
            {"state": 'walk',
             "x_speed": min(config.CAT_MAX_X_SPEED, config.CAT_WALK_ACCELERATION*3)}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.LEFT), 3,
            {"state": "stand"},
            {"state": 'walk',
             "x_speed": max(-config.CAT_MAX_X_SPEED, -config.CAT_WALK_ACCELERATION*3, -config.CAT_WALK_ACCELERATION*3)}))

    def test_speed_walk_update(self):
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.DOWN), 3,
            {"state": "walk",
             "x_speed": 5, "y_speed": 0},
            {"state": "walk",
             "x_speed": max(5-config.CAT_WALK_ACCELERATION*3, -config.CAT_MAX_X_SPEED)}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.UP), 1,
            {"state": "walk",
             "x_speed": 5, "y_speed": 10},
            {"state": 'jump',
             "x_speed": max(-config.CAT_MAX_X_SPEED, 5 - config.CAT_WALK_ACCELERATION), "y_speed": config.CAT_JUMP_SPEED}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.RIGHT), 1,
            {"state": "walk",
             "x_speed": 5, "y_speed": 10},
            {"state": 'walk',
             "x_speed": min(config.CAT_MAX_X_SPEED, config.CAT_WALK_ACCELERATION + 5), "y_speed": 10}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.LEFT), 1,
            {"state": "walk",
             "x_speed": 500, "y_speed": 10},
            {"state": 'walk',
             "x_speed": 500-config.CAT_CHANGE_DIRECTION_ACCELERATION,
             "y_speed": 10}))

    def test_speed_jump_update(self):
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.DOWN), 1,
            {"state": "jump",
             "x_speed": 5, "y_speed": 10},
            {"state": "fall",
             "x_speed": 5-config.CAT_WALK_ACCELERATION, "y_speed": 10+config.JUMP_GRAVITY}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.UP), 1,
            {"state": "jump",
             "x_speed": 5, "y_speed": 10},
            {"state": 'fall',
             "x_speed": 5 - config.CAT_WALK_ACCELERATION, "y_speed": 10 + config.JUMP_GRAVITY}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.RIGHT), 1,
            {"state": "jump",
             "x_speed": 5, "y_speed": 10,
             "x_acceleration": 0},
            {"state": 'fall',
             "x_speed": 5 + config.CAT_WALK_ACCELERATION, "y_speed": 10 + config.JUMP_GRAVITY}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.LEFT), 1,
            {"state": "jump",
             "x_speed": 500, "y_speed": 10},
            {"state": 'fall',
             "x_speed": 500 - config.CAT_CHANGE_DIRECTION_ACCELERATION, "y_speed": 10 + config.JUMP_GRAVITY}))

    def test_speed_fall_update(self):
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.DOWN), 1,
            {"state": "fall",
             "x_speed": 5, "y_speed": -500},
            {"state": "fall",
             "x_speed": 5-config.CAT_WALK_ACCELERATION, "y_speed": config.GRAVITY-500}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.UP), 1,
            {"state": "fall",
             "x_speed": 5, "y_speed": -1000},
            {"state": "fall",
             "x_speed": 5-config.CAT_WALK_ACCELERATION, "y_speed": config.GRAVITY-1000}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.RIGHT), 1,
            {"state": "fall",
             "x_speed": -500, "y_speed": -500,
             "x_acceleration": 0},
            {"state": "fall",
             "x_speed": config.CAT_CHANGE_DIRECTION_ACCELERATION-500, "y_speed": config.GRAVITY-500}))
        self._test_state_and_key(TestCatUpdateSpeedParams(
            PgKeyMock(PgKeyMock.LEFT), 1,
            {"state": "fall",
             "x_speed": -50, "y_speed": -500},
            {"state": "fall",
             "x_speed": -config.CAT_WALK_ACCELERATION-50, "y_speed": config.GRAVITY-500}))


    def test_position_update(self):
        self.cat.x_acceleration = 10
        self.cat.y_acceleration = 15
        self.cat.x_speed = 1
        self.cat.y_speed = 3
        self.cat.update_position(pg.sprite.Group(), 6, 5)
        self.assertEqual(self.cat.x_position, 15)
        self.assertEqual(self.cat.y_position, 20)
        self.assertEqual(self.cat.x_speed, 1)
        self.assertEqual(self.cat.y_speed, 3)
        self.assertEqual(self.cat.x_acceleration, 10)
        self.assertEqual(self.cat.y_acceleration, 15)

        # when we try to escape view rectangular
        self.cat.x_speed = -1
        self.cat.y_speed = 4
        self.cat.x_acceleration = -10
        self.cat.update_position(pg.sprite.Group(), 14, 3)
        self.assertEqual(self.cat.x_position, 14)
        self.assertEqual(self.cat.y_position, 32)
        self.assertEqual(self.cat.x_speed, 0)
        self.assertEqual(self.cat.y_speed, 4)
        self.assertEqual(self.cat.x_acceleration, 0)
        self.assertEqual(self.cat.y_acceleration, 15)
