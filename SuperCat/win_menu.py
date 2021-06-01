"""Module, containing win menu class."""
import pygame as pg

from . import config


class WinMenu:
    """
    Class for win menu.

    :param screen: Surface with whole screen
    :param name: Name of the winner
    """

    def __init__(self, screen: pg.Surface, name: str) -> None:
        """Create win menu object."""
        self.finished = False
        self.quit_pressed = False
        screen.fill(config.SKY_COLOR)
        offsets = [-30, 100]
        text_stings = [_("Player") + ' "' + name + '\" ' + _("won!"), _("Press ENTER to continue")]
        text_size = [45, 30]
        for offset, text, size in zip(offsets, text_stings, text_size):
            font = pg.font.SysFont('monospace', bold=True, size=size)
            text = font.render(text, True, config.TEXT_COLOR, config.TEXT_BACKGROUND_COLOR)
            text_rect = text.get_rect(center=(config.SCREEN_WIDTH / 2, config.SCREEN_HEIGHT / 2 + offset))
            screen.blit(text, text_rect)

    def update_events(self) -> None:
        """Catch win menu events."""
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    self.finished = True
                elif event.key == pg.K_ESCAPE:
                    self.finished = True
                    self.quit_pressed = True
            elif event.type == pg.QUIT:
                self.finished = True
                self.quit_pressed = True

    def mainloop(self) -> None:
        """Loop for win menu."""
        while not self.finished:
            self.update_events()
            pg.display.update()
