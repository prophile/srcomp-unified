"""Core competition functions."""

from copy import copy
import imp
import os
from subprocess import check_output
import sys

from sr.comp import arenas, matches, scores, teams, venue
from sr.comp.winners import compute_awards


def load_scorer(root):
    """
    Load the scorer module from Compstate repo.

    :param str root: The path to the compstate repo.
    """

    # Deep path hacks
    score_directory = os.path.join(root, 'scoring')
    score_source = os.path.join(score_directory, 'score.py')

    saved_path = copy(sys.path)
    sys.path.append(score_directory)

    imported_library = imp.load_source('score.py', score_source)

    sys.path = saved_path

    return imported_library.Scorer


class SRComp(object):
    """
    A class containing all the various parts of a competition.

    :param str root: The root path of the ``compstate`` repo.
    """

    def __init__(self, root):
        self.root = root

        self.state = check_output(('git', 'rev-parse', 'HEAD'),
                                  universal_newlines=True,
                                  cwd=root).strip()
        """The current commit of the Compstate repository."""

        self.teams = teams.load_teams(os.path.join(root, "teams.yaml"))
        """A :class:`collections.OrderedDict` mapping TLAs to
        :class:`sr.comp.teams.Team` objects."""

        scorer = load_scorer(root)
        self.scores = scores.Scores(root, self.teams.keys(), scorer)
        """A :class:`sr.comp.scores.Scores` instance."""

        self.arenas = arenas.load_arenas(os.path.join(root, "arenas.yaml"))
        """A :class:`collections.OrderedDict` mapping arena names to
        :class:`sr.comp.arenas.Arena` objects."""

        schedule_fname = os.path.join(root, "schedule.yaml")
        league_fname = os.path.join(root, "league.yaml")
        self.schedule = matches.MatchSchedule.create(schedule_fname,
                                                     league_fname, self.scores,
                                                     self.arenas, self.teams)
        """A :class:`sr.comp.matches.MatchSchedule` instance."""

        self.timezone = self.schedule.timezone
        """The timezone of the competition."""

        self.corners = arenas.load_corners(os.path.join(root, "arenas.yaml"))
        """A :class:`collections.OrderedDict` mapping corner numbers to
        :class:`sr.comp.arenas.Corner` objects."""

        self.awards = compute_awards(self.scores,
                                     self.schedule.final_match,
                                     self.teams,
                                     os.path.join(root, "awards.yaml"))
        """A :class:`dict` mapping :class:`sr.comp.winners.Award` objects to
        a :class:`list` of teams."""

        self.venue = venue.Venue(self.teams.keys(),
                                 os.path.join(root, "layout.yaml"),
                                 os.path.join(root, "shepherding.yaml"))
        """A :class:`sr.comp.venue.Venue` instance."""

        self.venue.check_staging_times(self.schedule.staging_times)

        pyver = sys.version_info
        if pyver[0] == 3 and (pyver < (3, 4, 4) or pyver == (3, 5, 0)):
            from warnings import warn
            warn("Python 3 < 3.4.4, 3.5.1 has a known issue with timezones that "
                 "have the same `dst()` and `utcoffset()` values (such as BST). "
                 "Using Python 2 instead is recommended. "
                 "See https://bugs.python.org/issue23600.")
