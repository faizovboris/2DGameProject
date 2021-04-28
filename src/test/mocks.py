import pygame as pg

class PgKeyMock:
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
    key_map = {LEFT: pg.K_LEFT,
               RIGHT: pg.K_RIGHT,
               UP: pg.K_UP,
               DOWN: pg.K_DOWN}

    def __init__(self, *keys):
        self.set(*keys)

    def __getitem__(self, key):
        return self.dictionary[key]

    def __setitem__(self, key, value):
        assert False

    def delete_all(self):
        self.dictionary = dict.fromkeys(PgKeyMock.key_map.values(), False)

    def set(self, *keys):
        self.delete_all()
        for key in keys:
            self.add(key)

    def add(self, key):
        self.dictionary[PgKeyMock.key_map[key]] = True