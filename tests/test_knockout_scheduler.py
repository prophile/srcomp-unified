
from collections import OrderedDict
from datetime import datetime, timedelta
import mock

from sr.comp.scores import TeamScore
from sr.comp.matches import Delay
from sr.comp.match_period import Match, MatchType
from sr.comp.knockout_scheduler import KnockoutScheduler, UNKNOWABLE_TEAM

def get_scheduler(matches = None, positions = None, \
                    knockout_points = None, league_game_points = None, \
                    delays = None):
    matches = matches or []
    delays = delays or []
    match_duration = timedelta(minutes = 5)
    league_game_points = league_game_points or {}
    knockout_points = knockout_points or {}
    if not positions:
        positions = OrderedDict()
        positions['ABC'] = 1
        positions['DEF'] = 2

    league_schedule = mock.Mock(matches = matches, delays = delays, \
                                match_duration = match_duration)
    league_scores = mock.Mock(positions = positions, game_points = league_game_points)
    knockout_scores = mock.Mock(ranked_points = knockout_points)
    scores = mock.Mock(league = league_scores, knockout = knockout_scores)

    period_config = {
        "description": "A description of the period",
        "start_time":   datetime(2014, 3, 27,  13),
        "end_time":     datetime(2014, 3, 27,  17, 30),
    }
    knockout_config = {
        'round_spacing': 30,
        'final_delay': 12,
        'single_arena': {
            'rounds': 3,
            'arenas': ["A"],
        },
    }
    config = {
        'match_periods': { 'knockout': [period_config] },
        'knockout': knockout_config,
    }
    arenas = ['A']
    scheduler = KnockoutScheduler(league_schedule, scores, arenas, config)
    return scheduler


def test_knockout_match_winners_empty():
    scheduler = get_scheduler()
    game = Match(2, 'A', [], None, None, None)
    winners = scheduler.get_winners(game)
    assert winners == [UNKNOWABLE_TEAM] * 2

def test_knockout_match_winners_simple():
    knockout_points = {
        ('A', 2): {
            'ABC': 1.0,
            'DEF': 2.0,
            'GHI': 3.0,
            'JKL': 4.0,
        }
    }
    scheduler = get_scheduler(knockout_points = knockout_points)

    game = Match(2, 'A', [], None, None, None)
    winners = scheduler.get_winners(game)

    assert set(winners) == set(['GHI', 'JKL'])

def test_knockout_match_winners_irrelevant_tie_1():
    knockout_points = {
        ('A', 2): {
            'ABC': 1.5,
            'DEF': 1.5,
            'GHI': 3,
            'JKL': 4,
        }
    }
    scheduler = get_scheduler(knockout_points = knockout_points)

    game = Match(2, 'A', [], None, None, None)
    winners = scheduler.get_winners(game)

    assert set(winners) == set(['GHI', 'JKL'])

def test_knockout_match_winners_irrelevant_tie_1():
    knockout_points = {
        ('A', 2): {
            'ABC': 1,
            'DEF': 2,
            'GHI': 3.5,
            'JKL': 3.5,
        }
    }
    positions = {
        'ABC': 1,
        'DEF': 2,
        'GHI': 3,
        'JKL': 4,
    }
    scheduler = get_scheduler(knockout_points = knockout_points, \
                                positions = positions)

    game = Match(2, 'A', [], None, None, None)
    winners = scheduler.get_winners(game)

    assert set(winners) == set(['GHI', 'JKL'])

def test_knockout_match_winners_tie():
    knockout_points = {
        ('A', 2): {
            'ABC': 1,
            'DEF': 2.5,
            'GHI': 2.5,
            'JKL': 4,
        }
    }
    # Deliberately out of order as some python implementations
    # use the creation order of the tuples as a fallback sort comparison
    positions = {
        'ABC': 1,
        'DEF': 4,
        'GHI': 3,
        'JKL': 2,
    }
    scheduler = get_scheduler(knockout_points = knockout_points, \
                                positions = positions)

    game = Match(2, 'A', [], None, None, None)
    winners = scheduler.get_winners(game)

    assert set(winners) == set(['GHI', 'JKL']), \
            "Should used the league positions to resolve the tie"


def test_first_round_before_league_end():
    positions = OrderedDict()
    positions['ABC'] = 1
    positions['CDE'] = 2
    positions['EFG'] = 3
    positions['GHI'] = 4

    # Fake a couple of league matches that won't have been scored
    matches = [
        {'A':Match(0, 'A', [], None, None, MatchType.league)},
        {'A':Match(1, 'A', [], None, None, MatchType.league)},
    ]
    scheduler = get_scheduler(matches, positions = positions)

    def seeder(*args):
        assert args[0] == 4, "Wrong number of teams"
        return [[0,1,2,3]]

    # Mock the random (even thought it's not really random)
    scheduler.R = mock.Mock()
    # Mock the seeder to make it less interesting
    with mock.patch('sr.comp.knockout.first_round_seeding') as first_round_seeding:
        first_round_seeding.side_effect = seeder
        scheduler.add_knockouts()

    knockout_rounds = scheduler.knockout_rounds
    period = scheduler.period

    assert len(knockout_rounds) == 1, "Should be finals only"
    finals = knockout_rounds[0]

    assert len(finals) == 1, "Should be one final"
    final = finals[0]
    final_teams = final.teams

    # No scores yet -- should just list as ???
    expected_teams = [UNKNOWABLE_TEAM] * 4

    assert expected_teams == final_teams, "Should not show teams until league complete"

def test_first_round():
    positions = OrderedDict()
    positions['ABC'] = 1
    positions['CDE'] = 2
    positions['EFG'] = 3
    positions['GHI'] = 4
    positions['IJK'] = 5
    positions['KLM'] = 6
    positions['MNO'] = 7
    positions['OPQ'] = 8

    # Fake a couple of league matches
    matches = [{},{}]
    scheduler = get_scheduler(matches, positions = positions)

    def seeder(*args):
        assert args[0] == 8, "Wrong number of teams"
        return [[0,1,2,3],[4,5,6,7]]

    # Mock the random (even thought it's not really random)
    scheduler.R = mock.Mock()
    # Mock the seeder to make it less interesting
    with mock.patch('sr.comp.knockout.first_round_seeding') as first_round_seeding:
        first_round_seeding.side_effect = seeder
        scheduler.add_knockouts()

    knockout_rounds = scheduler.knockout_rounds
    period = scheduler.period

    assert len(knockout_rounds) == 2, "Should be semis and finals"
    semis = knockout_rounds[0]

    assert len(semis) == 2, "Should be two semis"
    semi_0 = semis[0]
    semi_0_teams = semi_0.teams
    # Thanks to our mocking of the seeder...
    expected_0_teams = list(positions.keys())[:4]

    assert semi_0.num == 2, "Match number should carry on above league matches"
    assert semi_0.type == MatchType.knockout
    assert semi_0_teams == expected_0_teams

    period_matches = period.matches
    expected_matches = [{'A':m} for r in knockout_rounds for m in r]

    assert period_matches == expected_matches
    final = period_matches[2]['A']
    final_teams = final.teams

    assert final_teams == [UNKNOWABLE_TEAM] * 4

def test_timings_no_delays():
    positions = OrderedDict()
    for i in range(16):
        positions['team-{}'.format(i)] = i

    scheduler = get_scheduler(positions = positions)
    scheduler.add_knockouts()

    knockout_rounds = scheduler.knockout_rounds
    num_rounds = len(knockout_rounds)

    assert num_rounds == 3, "Should be quarters, semis and finals"

    start_times = [m['A'].start_time for m in scheduler.period.matches]

    expected_times = [
        # Quarter finals
        datetime(2014, 3, 27,  13,  0),
        datetime(2014, 3, 27,  13,  5),
        datetime(2014, 3, 27,  13, 10),
        datetime(2014, 3, 27,  13, 15),

        # 30 second gap

        # Semi finals
        datetime(2014, 3, 27,  13, 20, 30),
        datetime(2014, 3, 27,  13, 25, 30),

        # 30 second gap
        # bonus 12 second gap

        # Final
        datetime(2014, 3, 27,  13, 31, 12)
    ]

    assert expected_times == start_times, "Wrong start times"

def test_timings_with_delays():
    positions = OrderedDict()
    for i in range(16):
        positions['team-{}'.format(i)] = i

    delays = [
        Delay(time = datetime(2014, 3, 27,  13,  2),
              delay = timedelta(minutes = 5)),
        Delay(time = datetime(2014, 3, 27,  13, 12),
              delay = timedelta(minutes = 5))
    ]

    scheduler = get_scheduler(positions = positions, delays = delays)
    scheduler.add_knockouts()

    knockout_rounds = scheduler.knockout_rounds
    num_rounds = len(knockout_rounds)

    assert num_rounds == 3, "Should be quarters, semis and finals"

    start_times = [m['A'].start_time for m in scheduler.period.matches]

    expected_times = [
        # Quarter finals
        datetime(2014, 3, 27,  13,  0),
        datetime(2014, 3, 27,  13, 10), # affected by first delay only
        datetime(2014, 3, 27,  13, 20), # affected by both delays
        datetime(2014, 3, 27,  13, 25),

        # 30 second gap

        # Semi finals
        datetime(2014, 3, 27,  13, 30, 30),
        datetime(2014, 3, 27,  13, 35, 30),

        # 30 second gap
        # bonus 12 second gap

        # Final
        datetime(2014, 3, 27,  13, 41, 12)
    ]

    assert expected_times == start_times, "Wrong start times"

def test_timings_with_delays_during_gaps():
    positions = OrderedDict()
    for i in range(16):
        positions['team-{}'.format(i)] = i

    delays = [
        Delay(time = datetime(2014, 3, 27,  13, 20, 15),
              delay = timedelta(minutes = 5)),
        Delay(time = datetime(2014, 3, 27,  13, 36),
              delay = timedelta(minutes = 5))
    ]

    scheduler = get_scheduler(positions = positions, delays = delays)
    scheduler.add_knockouts()

    knockout_rounds = scheduler.knockout_rounds
    num_rounds = len(knockout_rounds)

    assert num_rounds == 3, "Should be quarters, semis and finals"

    start_times = [m['A'].start_time for m in scheduler.period.matches]

    expected_times = [
        # Quarter finals
        datetime(2014, 3, 27,  13,  0),
        datetime(2014, 3, 27,  13,  5),
        datetime(2014, 3, 27,  13, 10),
        datetime(2014, 3, 27,  13, 15),

        # 30 second gap
        # first delay

        # Semi finals
        datetime(2014, 3, 27,  13, 25, 30),
        datetime(2014, 3, 27,  13, 30, 30),

        # 30 second gap
        # bonus 12 second gap

        # Final
        datetime(2014, 3, 27,  13, 41, 12)
    ]

    assert expected_times == start_times, "Wrong start times"
