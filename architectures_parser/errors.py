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


class ArchitecturesParserError(Exception):
    """Base class for all exceptions in this project."""
    pass


class MissingPropertyError(ArchitecturesParserError):
    """Error for when an expected property is not present in the YAML."""

    def __init__(self, prop):
        super(MissingPropertyError, self).__init__(
            'Architecture specification is missing the {!r} property'.format(
                prop))
        self.property = prop


class UnsupportedBuildOnError(ArchitecturesParserError):
    """Error for when a requested architecture is not supported."""

    def __init__(self, build_on):
        super(UnsupportedBuildOnError, self).__init__(
            'build-on specifies no supported architectures: {!r}'.format(
                build_on))
        self.build_on = build_on


class IncompatibleArchitecturesStyleError(ArchitecturesParserError):
    """Error for when architectures mix incompatible styles."""

    def __init__(self):
        super(IncompatibleArchitecturesStyleError, self).__init__(
            "'architectures' must either be a list of strings or dicts, not "
            "both")
