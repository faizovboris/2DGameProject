#!/usr/bin/env python3
"""
Main module of game.
"""
import os
import pygame as pg
import gameplay
import level
import config


def main():
    """Main game function."""
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption("Super Cat")
    screen = pg.display.set_mode(config.SCREEN_SIZE)
    game = gameplay.Gameplay(level.Level(), screen)
    game.mainloop()


if __name__ == '__main__':
    main()
    pg.quit()
