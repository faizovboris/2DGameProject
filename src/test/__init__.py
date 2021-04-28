import pygame as pg
import config
import unittest

def setUpModule():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(("Super Cat"))
    screen = pg.display.set_mode(config.SCREEN_SIZE)

def tearDownModule():
    pg.quit()