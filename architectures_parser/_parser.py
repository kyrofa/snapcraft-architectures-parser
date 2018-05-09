# -*- Mode:Python; indent-tabs-mode:nil; tab-width:4 -*-
#
# Copyright (C) 2018 Canonical Ltd
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 3 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import yaml

from . import errors
from ._architecture import Architecture
from ._build_instance import BuildInstance


def determine_build_instances(snapcraft_yaml, supported_architectures):
    """Extract desired builds from snapcraft.yaml

    :param str snapcraft_yaml: The contents of a snapcraft.yaml, as a string
    :param list supported_architectures: List of supported architectures,
                                         sorted by priority. In cases where
                                         multiple architectures are suitable,
                                         the earliest one in this list will be
                                         selected.
    :returns: List of BuildInstances

    This function supports parsing the 'architectures' keyword from the
    snapcraft.yaml according to the spec documented here:
    https://forum.snapcraft.io/t/architectures/4972
    """
    data = yaml.safe_load(snapcraft_yaml)
    architectures_list = data.get('architectures')

    if architectures_list:
        # First, determine what style we're parsing. A list of strings, or a
        # list of dicts?
        if all(isinstance(i, str) for i in architectures_list):
            # If a list of strings (old style), then that's only a single item
            architectures = [Architecture(build_on=architectures_list)]
        elif all(isinstance(i, dict) for i in architectures_list):
            # If a list of dicts (new style) that's multiple items
            architectures = [
                Architecture.from_dict(a) for a in architectures_list]
        else:
            # If a mix of both, bail. We can't reasonably handle it.
            raise errors.IncompatibleArchitecturesStyleError()
    else:
        # If no architectures are specified, build one for each supported
        # architecture
        architectures = [
            Architecture(build_on=a) for a in supported_architectures]

    build_instances = []
    for architecture in architectures:
        build_instances.append(
            BuildInstance(architecture, supported_architectures))

    return build_instances
