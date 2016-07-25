"""Team metadata library."""

from collections import namedtuple

from sr.comp import yaml_loader


_Team = namedtuple('Team', ['tla', 'name', 'rookie',
                            'dropped_out_after'])
class Team(_Team):
    def is_still_around(self, match_number):
        """
        Check if this team is still around at a certain match.

        :param int match_number: The number of the match to check.
        :returns: ``True`` if the team is still playing.
        """

        if self.dropped_out_after is None:
            return True
        else:
            return match_number <= self.dropped_out_after


def load_teams(filename):
    """
    Load teams from a YAML file.

    :param str filename: The filename of the YAML file to load.
    :return: A dictionary mapping TLAs to :class:`Team` objects.
    """

    data = yaml_loader.load(filename)

    teams = {}
    for tla, info in data['teams'].items():
        tla = tla.upper()
        teams[tla] = Team(tla=tla, name=info['name'],
                          rookie=info.get('rookie', False),
                          dropped_out_after=info.get('dropped_out_after'))

    return teams
