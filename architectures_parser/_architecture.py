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

class Architecture:
    """This class represents a single entry in the 'architectures' list

    It has three useful attributes:

      - build_on: The 'build-on' property of this entry
      - run_on: The 'run-on' property of this entry
      - build_error: The 'build-error' property of this entry
    """

    @classmethod
    def from_dict(cls, properties):
        """Create a new Architecture from a dict

        :param dict properties: Properties of a single entry in the
                                'architectures' list
        """
        run_on = properties.get('run-on')
        build_error = properties.get('build-error')

        try:
            build_on = properties['build-on']
        except KeyError as e:
            raise errors.MissingPropertyError(e.args[0])

        return cls(build_on=build_on, run_on=run_on, build_error=build_error)

    def __init__(self, build_on, run_on=None, build_error=None):
        """Create a new Architecture

        :param str/list build_on: build-on property from YAML
        :param str/list run_on: run-on property from YAML (defaults to
                                build-on)
        :param str build_error: build-error property from YAML
        """

        self.build_error = build_error

        if isinstance(build_on, str):
            self.build_on = [build_on]
        else:
            self.build_on = build_on

        # If there is no run_on, it defaults to the value of build_on
        if not run_on:
            self.run_on = self.build_on
        elif isinstance(run_on, str):
            self.run_on = [run_on]
        else:
            self.run_on = run_on
