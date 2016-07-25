Introduction
============

As with many league structures, the SR league (as specified in the rulebook_)
separates the notion of *game points* and *league points*. As teams take part
in games, they each acquire a certain score in each game; their position
relative to other teams in the same game determines the number of league
points they get.

In the most basic wins/losses setup in a typical 2-player-game league, the
usual distribution is 1 league point for a win and 0 for a loss, making league
points equivalent to wins. In 2-player games that have ties, this might go to
3 points for a win, 1 point for a tie and 0 points for a loss.

The SR game, however, is unusual in that each game has 4 teams taking part.
Giving league points only to the team that comes first would not create
sufficient separation in the league.

The League Points algorithm
----------------------------

The basic league points algorithm is as follows. Each match is worth 20 league
points in total, between all 4 teams. 8 points are awarded to the team in 1\ 
:sup:`st` place, 6 to the team in 2\ :sup:`nd` place, 4 to the team in 3\ 
:sup:`rd` and 2 to the team in last place.

In case of a tie, the points between tied teams are divided evenly. For
instance, in a 2-way tie for 1\ :sup:`st` place, there are a total of (8 + 6 =
14) points available, so both teams are awarded 7 points. Despite the
division, in all cases the awarded points are an exact integer.

Disqualifications
-----------------

Occasionally, teams are disqualified from matches. This can be a failure to
appear (where, naturally, they should not be awarded league points), safety
issues, or foul play.

In the event of a team's disqualification, two changes are made to the league
points algorithm:

 1. The disqualified team is considered to have fewer game points than any
    other team—that is, even if another team scored 0 game points, the
    disqualified team would place lower.
 2. After league points are distributed, the awarded league points are set to 0
    for the disqualified team.

.. _rulebook: https://www.studentrobotics.org/resources/2015/rulebook.pdf

