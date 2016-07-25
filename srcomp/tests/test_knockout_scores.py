
from collections import OrderedDict

from sr.comp.scores import KnockoutScores

def test_positions_simple():
    knockout_points = {
        'ABC': 1.0,
        'DEF': 2.0,
        'GHI': 3.0,
        'JKL': 4.0,
    }

    positions = KnockoutScores.calculate_ranking(knockout_points, {})

    expected = OrderedDict([
        ('JKL', 1),
        ('GHI', 2),
        ('DEF', 3),
        ('ABC', 4),
    ])

    assert expected == positions

def test_positions_tie_bottom():
    knockout_points = {
        'ABC': 1.5,
        'DEF': 1.5,
        'GHI': 3,
        'JKL': 4,
    }

    positions = KnockoutScores.calculate_ranking(knockout_points, {})

    expected = OrderedDict([
        ('JKL', 1),
        ('GHI', 2),
        ('ABC', 3),
        ('DEF', 3),
    ])

    assert expected == positions

def test_positions_tie_top_with_league_positions():
    knockout_points = {
        'ABC': 1,
        'DEF': 2,
        'GHI': 3.5,
        'JKL': 3.5,
    }
    league_positions = {
        'ABC': 1,
        'DEF': 2,
        'GHI': 3,
        'JKL': 4,
    }
    positions = KnockoutScores.calculate_ranking(knockout_points, league_positions)

    # Tie should be resolved by league positions
    expected = OrderedDict([
        ('GHI', 1),
        ('JKL', 2),
        ('DEF', 3),
        ('ABC', 4),
    ])

    assert expected == positions

def test_knockout_match_winners_tie():
    knockout_points = {
        'ABC': 1,
        'DEF': 2.5,
        'GHI': 2.5,
        'JKL': 4,
    }
    # Deliberately out of order as some python implementations
    # use the creation order of the tuples as a fallback sort comparison
    league_positions = {
        'ABC': 1,
        'DEF': 4,
        'GHI': 3,
        'JKL': 2,
    }
    positions = KnockoutScores.calculate_ranking(knockout_points, league_positions)

    # Tie should be resolved by league positions
    expected = OrderedDict([
        ('JKL', 1),
        ('GHI', 2),
        ('DEF', 3),
        ('ABC', 4),
    ])

    assert expected == positions
