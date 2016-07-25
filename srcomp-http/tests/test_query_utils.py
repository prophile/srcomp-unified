import mock

from sr.comp.http.query_utils import get_scores
from sr.comp.match_period import Match, MatchType


GAME_POINTS_DUMMY = 'test game_points for: '
POSITIONS_DUMMY = 'test positions for: '
RANKED_DUMMY = 'test ranked for: '
RESOLVED_DUMMY = 'test resolved for: '


def make_session_scores(arena, num):
    key = (arena, num)
    scores = mock.Mock()
    scores.game_points = {key: GAME_POINTS_DUMMY + str(key)}
    scores.game_positions = {key: {num: [POSITIONS_DUMMY + repr(arena)]}}
    scores.ranked_points = {key: RANKED_DUMMY + str(key)}
    scores.resolved_positions = {key: {RESOLVED_DUMMY + repr(arena): num}}
    return scores


def build_scores():
    scores = mock.Mock()
    scores.league = make_session_scores('A', 0)
    scores.knockout = make_session_scores('A', 1)
    scores.tiebreaker = make_session_scores('A', 2)
    return scores


def build_match(num, arena, teams=None, start_time=None, end_time=None,
                type_=None, use_resolved_ranking=False):
    return Match(num, 'Match {n}'.format(n=num), arena, teams, start_time,
                 end_time, type_, use_resolved_ranking)


def test_league_match():
    scores = build_scores()
    info = get_scores(scores, build_match(num=0, arena='A',
                                          type_=MatchType.league))
    expected = {
        "game": GAME_POINTS_DUMMY + "('A', 0)",
        "league": RANKED_DUMMY + "('A', 0)",
        "ranking": { POSITIONS_DUMMY + "'A'": 0 },
    }
    assert expected == info


def test_knockout_match():
    scores = build_scores()
    info = get_scores(scores, build_match(num=1, arena='A',
                                          type_=MatchType.knockout,
                                          use_resolved_ranking=True))
    expected = {
        "game": GAME_POINTS_DUMMY + "('A', 1)",
        "normalised": RANKED_DUMMY + "('A', 1)",
        "ranking": { RESOLVED_DUMMY + "'A'": 1 },
    }
    assert expected == info


def test_finals_match():
    scores = build_scores()
    info = get_scores(scores, build_match(num=1, arena='A',
                                          type_=MatchType.knockout,
                                          use_resolved_ranking=False))
    expected = {
        "game": GAME_POINTS_DUMMY + "('A', 1)",
        "normalised": RANKED_DUMMY + "('A', 1)",
        "ranking": { POSITIONS_DUMMY + "'A'": 1 },
    }
    assert expected == info


def test_tiebreaker_match():
    scores = build_scores()
    info = get_scores(scores, build_match(num=2, arena='A',
                                          type_=MatchType.tiebreaker))
    expected = {
        "game": GAME_POINTS_DUMMY + "('A', 2)",
        "normalised": RANKED_DUMMY + "('A', 2)",
        "ranking": { POSITIONS_DUMMY + "'A'": 2 },
    }
    assert expected == info


def test_no_match():
    scores = build_scores()
    info = get_scores(scores, build_match(num=1, arena='B'))
    expected = None
    assert expected == info
