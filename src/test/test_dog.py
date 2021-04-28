import unittest
from dog import Dog
from gameplay import Gameplay
import config
import pygame as pg
import os

class TestDog(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.images_holder = Gameplay.load_all_images('./images')

    def setUp(self):
        self.dog = Dog(self.images_holder, 10, 5, 0, 100, 1, 5)

    def test_speed_update(self):
        pass

    def test_position_update(self):
        pass


if __name__ == '__main__':
    unittest.main()
