"""Module, containing implementaion of sound manager."""
import os
import pygame as pg


class SoundManager(object):
    """
    Class for sound manager.

    :param music_folder: Path to folder with music
    """

    def __init__(self, music_folder: str) -> None:
        """Create SoundManager object."""
        self.music_data = {}
        for sound_file in os.listdir(music_folder):
            name, ext = os.path.splitext(sound_file)
            self.music_data[name] = pg.mixer.Sound(os.path.join(music_folder, sound_file))
        self.background_music = None

    def set_background_music(self, music_key: str) -> None:
        """
        Set background music.

        :param music_key: id of music file
        """
        if music_key not in self.music_data.keys():
            return
        if self.background_music:
            self.music_data[self.background_music].stop()
        self.music_data[music_key].play(-1)
        self.music_data[music_key].set_volume(0.1)
        self.background_music = music_key

    def set_effect(self, music_key: str) -> None:
        """
        Set current music effect.

        :param music_key: id of music file
        """
        if music_key not in self.music_data.keys():
            return
        self.music_data[music_key].play()

    def stop_music(self) -> None:
        """Stop all music."""
        pg.mixer.music.stop()
        if self.background_music:
            self.music_data[self.background_music].stop()
            self.background_music = None
