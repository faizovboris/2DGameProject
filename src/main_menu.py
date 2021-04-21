"""Module, containing main menu class."""
import pygame as pg

import config


class MainMenu:
    """
    Class for main menu.

    :param screen: Surface with whole screen
    """

    def __init__(self, screen: pg.Surface) -> None:
        """Create main menu object."""
        self.screen = screen
        self.finished = False
        self.quit_pressed = False
        self.input_text = ""
        self.text_color = (255, 255, 255)
        self.text_background = (255, 100, 100)
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
        while not self.finished:
            self.update_events()
            self.update_input_text()
            pg.display.update()
