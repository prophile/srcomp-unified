"""Conversions of game points into league points."""

from __future__ import print_function

from collections import defaultdict


def calc_positions(zpoints, dsq_list=()):
    """
    Calculate positions from a map of zones to in-game points.

    Parameters
    ----------
    zpoints : dict
        A mapping from some key (typically a zone or corner name) to game
        points (usually a numeric type, but can be any type that is comparable
        and usable as a key for dictionaries).
    dsq_list : list
        If provided, is a :py:class:`list` of keys of teams or zones that have
        been disqualified and are therefore considered below last place.

    Returns
    -------
    dict
        A mapping from positions to an iterable of teams in that position.

    Note
    ----
       In case of a tie, both teams are awarded the same position, as is usual
       in sport. That is, if team A has 3 points, team B has 3 points and team
       C has 1 point, then teams A and B are both awarded 1\ :sup:`st`, and C
       is awarded 3\ :sup:`rd`.

    Examples
    --------
    Some examples of usage are shown below:

    >>> calc_positions({'A': 3, 'B': 3, 'C': 1})
    {1: {'A', 'B'}, 3: {'C'}}

    >>> calc_positions({'A': 3, 'B': 3, 'C': 0, 'D': 0}, ['A', 'C'])
    {1: {'B'}, 2: {'D'}, 3: {'A', 'C'}}
    """

    pos_map = {}
    points_map = defaultdict(set)

    for zone, points in zpoints.items():
        if zone in dsq_list:
            points = -1
        points_map[points].add(zone)

    position = 1
    for points in sorted(list(points_map.keys()), reverse=True):
        pos_map[position] = points_map[points]
        position += len(points_map[points])

    return pos_map


def calc_ranked_points(pos_map, dsq_list=()):
    """
    Calculate SR league points from a mapping of positions to teams.

    Parameters
    ----------
    pos_map : dict
        A mapping from positions (integers indicating ending position, such as
        1 for 1\ :sup:`st`, 3 for 3\ :sup:`rd` etc) to some iterable of teams
        or zones in that position.
    dsq_list : list
        If provided, is a :py:class:`list` of teams or zones that are
        considered to be disqualified.

    Returns
    -------
    dict
        A mapping from zones/teams to SR league points.

    Note
    ----
    League points, and their calculation, are described in detail in the SR
    rulebook_.

    .. _rulebook: https://www.studentrobotics.org/resources/2015/rulebook.pdf

    Examples
    --------
    Some examples of usage are shownn below.

    >>> calc_ranked_points({1: ['A'], 2: ['B'], 3: ['C'], 4: ['D']})
    {'A': 8, 'B': 6, 'C': 4, 'D': 2}

    >>> calc_ranked_points({1: ['A', 'B'], 2: ['C', 'D']})
    {'A': 7, 'B': 7, 'C': 3, 'D': 4}

    >>> calc_ranked_points({1: ['B'], 2: ['D'], 3: ['A', 'C']}, ['A', 'C'])
    {'A': 0, 'B': 8, 'C': 0, 'D': 6}
    """

    rpoints = {}

    for pos, zones in pos_map.items():
        # remove any that are dsqaulified
        # note that we do this before working out the ties, so that any
        # dsq tie members are removed from contention
        zones = [z for z in zones if z not in dsq_list]
        if len(zones) == 0:
            continue

        # max points is 8, decreases by two for subsequent positions. pos is
        # 1-indexed, hence the subtraction
        points = 8 - 2*(pos - 1)
        # Now that we have the value for this position if it were not a tie,
        # we need to allow for ties. In case of a tie, the available points
        # for all the places used are shared by all those thus placed.
        # Eg: three first places get 6pts each (8+6+4)/3.
        # Rather than generate a list and average it, it's quicker to just
        # do some maths using the max value and the length of the list
        points = points - (len(zones) - 1)
        for zone in zones:
            rpoints[zone] = points

    # those that were dsq get 0
    for disqualified_zone in dsq_list:
        rpoints[disqualified_zone] = 0

    return rpoints


def get_ranked_points(zpoints, dsq=()):
    """
    Compute, from a mapping of teams to game points, the teams' league points.

    This is a convenience wrapper around `calc_positions` and
    `calc_rank_points`.

    Examples
    --------
    An example of usage is shown below.

    >>> get_ranked_points({'A': 1, 'B': 3, 'C': 3, 'D': 4}, ['A'])
    {'A': 0, 'B': 5, 'C': 5, 'D': 8}
    """

    pos_map = calc_positions(zpoints, dsq)
    rpoints = calc_ranked_points(pos_map, dsq)
    return rpoints


def _demo():
    """Run a quick demo of this module."""

    scores = {'ABC': 12,
              'DEF':  3,
              'ABC2': 4,
              'JLK': 10}

    dsq = []

    print('Original scores:', scores)
    ranked_scores = get_ranked_points(scores, dsq)
    print('Ranked scores:', ranked_scores)

    dsq = ['ABC']

    print("And now disqulifying 'ABC'.")
    ranked_scores = get_ranked_points(scores, dsq)
    print('Ranked scores:', ranked_scores)


if __name__ == '__main__':
    _demo()
