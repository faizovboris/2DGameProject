"""Custom mock objects."""
import pygame as pg


class PgKeyMock:
    """Mock object for imitating interactig with keyboard."""

    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    key_map = {LEFT: pg.K_LEFT,
               RIGHT: pg.K_RIGHT,
               UP: pg.K_UP,
               DOWN: pg.K_DOWN}

    def __init__(self, *keys):
        """Make mock with raised keyset."""
        self.set(*keys)

    def __getitem__(self, key):
        """Get value of key."""
        return self.dictionary[key]

    def delete_all(self):
        """Reset all keys."""
        self.dictionary = dict.fromkeys(PgKeyMock.key_map.values(), False)

    def set(self, *keys):
        """Set set of keys."""
        self.delete_all()
        for key in keys:
            self.add(key)

    def add(self, key):
        """Add key pressure."""
        self.dictionary[PgKeyMock.key_map[key]] = True
