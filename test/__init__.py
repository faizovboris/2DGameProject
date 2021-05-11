"""Tests for SuperCat."""
import pygame as pg
import os
import SuperCat.config as config


def setUpModule():
    """
    Set up testing environment at the beginning of testing module.

    :return:
    """
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(("Super Cat"))
    pg.display.set_mode(config.SCREEN_SIZE)


def tearDownModule():
    """
    Clear testing environment at the end of testing module.

    :return:
    """
    pg.quit()
