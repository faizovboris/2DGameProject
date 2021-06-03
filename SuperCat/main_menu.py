"""Module, containing main menu class."""
import pygame as pg

from . import config
from . import sound_manager


class MainMenu:
    """
    Class for main menu.

    :param screen: Surface with whole screen
    :param sounds: Sound Manager object
    :param best_score: Value of best score
    """

    def __init__(self, screen: pg.Surface, sounds: sound_manager.SoundManager, best_score: int) -> None:
        """Create main menu object."""
        self.screen = screen
        self.sounds = sounds
        self.finished = False
        self.quit_pressed = False
        self.input_text = ""
        self.text_color = config.TEXT_COLOR
        self.text_background = config.TEXT_BACKGROUND_COLOR
        self.max_text_len = 10
        self.padding = 5
        self.screen.fill(config.SKY_COLOR)
        self.font = pg.font.SysFont('monospace', bold=True, size=50)
        self.input_text_rendered = self.font.render(self.input_text, True, self.text_color, self.text_background)
        text_width = self.max_text_len * 30 + self.padding * 2
        text_height = self.input_text_rendered.get_height() + self.padding * 2
        self.input_text_image = pg.Surface((text_width, text_height), pg.SRCALPHA)

        text1_rendered = self.font.render(_("Name:"), True, self.text_color, self.text_background)
        widget_position = ((self.screen.get_width() - text_width) / 2,
                           (self.screen.get_height() - text_height) / 2 - text_height)
        self.screen.blit(text1_rendered, widget_position)

        for i, text in enumerate([_("^ Jump"), _("> Right"), _("< Left")]):
            text1_rendered = self.font.render(text, True, self.text_color, self.text_background)
            widget_position = (100, self.screen.get_height() - text_height * (i + 1))
            self.screen.blit(text1_rendered, widget_position)

        score_text = _("BEST SCORE:") + '{:06d}'.format(best_score)
        score_text = self.font.render(score_text, True, self.text_color, self.text_background)
        self.screen.blit(score_text, config.SCORE_POSITION)

    def update_input_text(self):
        """Update main menu input text."""
        self.input_text_rendered = self.font.render(self.input_text, True, self.text_color, self.text_background)
        self.input_text_image.fill(self.text_background)
        self.input_text_image.blit(self.input_text_rendered, (self.padding, self.padding))
        pg.draw.rect(self.input_text_image, self.text_color, self.input_text_image.get_rect().inflate(-2, -2), 4)
        widget_position = ((self.screen.get_width() - self.input_text_image.get_width()) / 2,
                           (self.screen.get_height() - self.input_text_image.get_height()) / 2)
        self.screen.blit(self.input_text_image, widget_position)

    def update_events(self) -> None:
        """Catch main menu events."""
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if len(self.input_text) > 0:
                        self.finished = True
                elif event.key == pg.K_ESCAPE:
                    self.finished = True
                    self.quit_pressed = True
                elif event.key == pg.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]
                else:
                    self.input_text += event.unicode
                    self.input_text = self.input_text[:self.max_text_len]
            elif event.type == pg.QUIT:
                self.finished = True
                self.quit_pressed = True

    def mainloop(self) -> None:
        """Loop for main menu."""
        self.sounds.set_background_music('theme')
        while not self.finished:
            self.update_events()
            self.update_input_text()
            pg.display.update()
        self.sounds.stop_music()
