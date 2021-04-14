#!/usr/bin/env python3
"""Main module of game."""
import os
import pygame as pg

import main_menu
import gameplay
import level
import config


def main():
    """Application main function."""
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption("Super Cat")
    screen = pg.display.set_mode(config.SCREEN_SIZE)
    while True:
        menu = main_menu.MainMenu(screen)
        menu.mainloop()
        if menu.quit_pressed:
            break
        game = gameplay.Gameplay(level.Level("level_1"), screen)
        game.mainloop()
        if game.quit_pressed:
            break


if __name__ == '__main__':
    main()
    pg.quit()
