import unittest
from SuperCat.scorer import ScorerObject


class TestScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = ScorerObject()

    def test_init_score_zero(self):
        self.assertEqual(self.scorer.get_score(), 0)

    def test_moving_score(self):
        self.scorer.update_max_position(100)
        self.scorer.update_max_position(50)
        self.scorer.update_max_position(150)
        self.scorer.update_max_position(100)
        self.assertEqual(self.scorer.get_score(), 150)

    def test_adding_score(self):
        self.scorer.add_score(42)
        self.assertEqual(self.scorer.get_score(), 42)
