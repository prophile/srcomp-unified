import unittest

from sr.comp import ranker


simple_data = { '0': 3, '1': 2, '2': 1, '3': 0 }
simple_pos = { 1: set(['0']), 2: set(['1']), 3: set(['2']), 4: set(['3']) }
simple_points = { '0': 8, '1': 6, '2': 4, '3': 2 }

dsq_data = { '0': 3, '1': 2, '2': 1, '3': 0 }
dsq_dsq = [ '0', '2' ]
dsq_pos = { 1: set(['1']), 2: set(['3']), 3: set(['0', '2']) }
dsq_points = { '0': 0, '1': 8, '2': 0, '3': 6 }

tie1_data = { '0': 3, '1': 3, '2': 0, '3': 0 }
tie1_pos = { 1: set(['1', '0']), 3: set(['3', '2']) }
tie1_points = { '0': 7, '1': 7, '2': 3, '3': 3 }

tie2_data = { '0': 3, '1': 3, '2': 0, '3': 0 }
tie2_dsq = [ '0', '2' ]
tie2_pos = { 1: set(['1']), 2: set(['3']), 3: set(['0', '2']) }
tie2_points = { '0': 0, '1': 8, '2': 0, '3': 6 }


class PositionsTests(unittest.TestCase):
    def test_simple(self):
        pos = ranker.calc_positions(simple_data, [])
        assert simple_pos == pos, "Wrong positions"

    def test_simple_no_dsq(self):
        pos = ranker.calc_positions(simple_data)
        assert simple_pos == pos, "Wrong positions"

    def test_tie(self):
        pos = ranker.calc_positions(tie1_data, [])
        assert tie1_pos == pos, "Wrong positions"

    def test_tie_no_dsq(self):
        pos = ranker.calc_positions(tie1_data)
        assert tie1_pos == pos, "Wrong positions"

    def test_dsq(self):
        pos = ranker.calc_positions(dsq_data, dsq_dsq)
        assert dsq_pos == pos, "Wrong positions"

    def test_dsq_tie(self):
        pos = ranker.calc_positions(tie2_data, tie2_dsq)
        assert tie2_pos == pos, "Wrong positions"


class RankedPointsTests(unittest.TestCase):
    def test_simple(self):
        points = ranker.calc_ranked_points(simple_pos, [])
        assert simple_points == points, "Wrong points"

    def test_simple_no_dsq(self):
        points = ranker.calc_ranked_points(simple_pos)
        assert simple_points == points, "Wrong points"

    def test_tie(self):
        points = ranker.calc_ranked_points(tie1_pos, [])
        assert tie1_points == points, "Wrong points"

    def test_tie_no_dsq(self):
        points = ranker.calc_ranked_points(tie1_pos)
        assert tie1_points == points, "Wrong points"

    def test_dsq_tie(self):
        points = ranker.calc_ranked_points(tie2_pos, tie2_dsq)
        assert tie2_points == points, "Wrong points"
