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


from architectures_parser import errors

class BuildInstance:
    """This class represents a single snap that should be built

    It has two useful attributes:

      - architecture: The architecture that should be used to build the snap
      - required: Whether or not failure to build should cause the entire set
                  to fail
    """

    def __init__(self, architecture, supported_architectures):
        """Construct a new BuildInstance

        :param Architecture architecture: Architecture instance
        :param list supported_architectures: List of supported architectures,
                                             sorted by priority
        """

        try:
            self.architecture = next(
                arch for arch in supported_architectures
                if arch in architecture.build_on)
        except StopIteration:
            raise errors.UnsupportedBuildOnError(architecture.build_on)

        self.required = architecture.build_error != 'ignore'
