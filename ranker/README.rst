Ranker
======

|Build Status|

Given a collection of entrants and their scores, it will sort them and
return their ranked points

The mechanism used to alocate the ranked points is (quote taken from the
`Student Robotics <https://www.studentrobotics.org>`__
`rulebook <https://www.studentrobotics.org/docs/rules>`__).

    The team with the **most** game points will be awarded 8 points
    towards the competition league. The team with the second most will
    be awarded 6. The team with the third most will be awarded 4 points,
    and the team with the fewest game points will be awarded 2 points.
    Teams whose robot was not entered into the round, or who were
    disqualified from the round, will be awarded no points.

    Tied robots will be awarded the average of the points that their
    combined positions would be awarded. Thus, three robots tied for
    first place would receive 6 points each (since this is
    ``(8+6+4)/3``).

As a result, the ranked points for an entrant (team) might not be an
integer. However, for 4 entrants the value will always be an integer.

It supports Python 2.7 and 3.x.

Tests
~~~~~

Tests can be run by running ``./run-tests``, which relies on nose.

.. |Build Status| image:: https://travis-ci.org/PeterJCLaw/ranker.png
   :target: https://travis-ci.org/PeterJCLaw/ranker
