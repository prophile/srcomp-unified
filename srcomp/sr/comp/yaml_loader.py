"""
YAML loading routines.

This includes parsing of dates and times properly, and also ensures the C YAML
loader is used which is necessary for optimum performance.
"""

import dateutil.tz
import dateutil.parser
import yaml

try:
    from yaml import CLoader as YAML_Loader
except ImportError:
    from yaml import Loader as YAML_Loader
    from warnings import warn
    warn("Using pure-python PyYAML (without libyaml)."
         " srcomp reads many YAML files, this is liable to be very slow. "
         "Installing libyaml is highly recommended.")


def time_constructor(loader, node):
    return dateutil.parser.parse(node.value)


def add_time_constructor(loader):
    loader.add_constructor("tag:yaml.org,2002:timestamp", time_constructor)


add_time_constructor(YAML_Loader)


def load(file_path):
    """
    Load a YAML fie and return the results.

    :param str file_path: The path to the YAML file.
    :return: The parsed contents.
    """
    with open(file_path, 'r') as f:
        return yaml.load(f, Loader=YAML_Loader)
