import unittest
from SuperCat.counter import Counter


class TestCounter(unittest.TestCase):
    def setUp(self):
        self.counter = Counter()

    def test_init_score_zero(self):
        self.assertEqual(self.counter.get_score(), 0)

    def test_moving_score(self):
        self.counter.update_max_position(100)
        self.counter.update_max_position(50)
        self.counter.update_max_position(150)
        self.counter.update_max_position(100)
        self.assertEqual(self.counter.get_score(), 150)

    def test_adding_score(self):
        self.counter.add_score(42)
        self.assertEqual(self.counter.get_score(), 42)
