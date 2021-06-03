#!/usr/bin/env python3
"""Main module of game."""
import os
import gettext
import pygame as pg

from . import main_menu, win_menu
from . import gameplay
from . import level
from . import sound_manager
from . import scorer
from . import config

package_directory = os.path.dirname(os.path.abspath(__file__))


def main():
    """Application main function."""
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pg.init()
    pg.display.set_caption(_("Super Cat"))
    screen = pg.display.set_mode(config.SCREEN_SIZE)
    sounds = sound_manager.SoundManager(os.path.join(package_directory, 'music'))
    sounds.set_background_music('theme')
    path_to_score = os.path.join(package_directory, 'best_score.txt')
    while True:
        best_score = scorer.ScorerObject.get_best_score(path_to_score)
        menu = main_menu.MainMenu(screen, best_score)
        menu.mainloop()
        if menu.quit_pressed:
            break
        game = gameplay.Gameplay(level.Level(os.path.join(package_directory, 'level_1'), sounds),
                                 screen, os.path.join(package_directory, 'images'))
        game.mainloop()
        game.cur_level.cur_scorer.update_best_score(path_to_score)
        if game.quit_pressed:
            break
        if game.win:
            win = win_menu.WinMenu(screen, menu.input_text)
            win.mainloop()
            if win.quit_pressed:
                break
    sounds.stop_music()


if __name__ == '__main__':
    gettext.install("main", package_directory, names=("ngettext",))
    main()
    pg.quit()
