"""Module, containing implementaion of game scorer."""
import os
import pygame as pg

from . import config


class ScorerObject(object):
    """Class for scoring game."""

    def __init__(self) -> None:
        """Create ScorerObject object."""
        self.score = 0
        self.max_position = 0
        self.font = pg.font.SysFont('monospace', bold=True, size=30)

    def draw_score(self, screen: pg.Surface) -> None:
        """
        Draw score on screen.

        :param screen: Surface with whole screen
        """
        text = _("SCORE:") + '{:06d}'.format(int(self.score))
        text = self.font.render(text, True, config.TEXT_COLOR)
        screen.blit(text, config.SCORE_POSITION)

    def update_max_position(self, cur_position: int) -> None:
        """
        Update score with max position.

        :param cur_position: current cat position
        """
        add_score = max(0, cur_position - self.max_position)
        self.add_score(add_score)
        self.max_position = max(self.max_position, cur_position)

    def add_score(self, add_score: int) -> None:
        """
        Add score.

        :param add_score: amount of score to add
        """
        self.score += add_score

    def get_score(self) -> None:
        """Get current score."""
        return self.score

    @staticmethod
    def get_best_score(filename: str) -> int:
        """
        Get current best score.
        
        :param filename: path to file with best score
        """
        best_score = 0
        if os.path.exists(filename):
            with open(filename, "r") as fr:
                try:
                    best_score = int(fr.read())
                except:
                    best_score = 0
        return best_score

    def update_best_score(self, filename):
        """
       Update current best score.
        
        :param filename: path to file with best score
        """
        best_score = max(self.get_best_score(filename), int(self.score))
        with open(filename, "w") as fw:
            fw.write(str(best_score))
