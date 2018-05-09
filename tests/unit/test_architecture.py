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


from architectures_parser._architecture import Architecture
from architectures_parser import errors

from testtools.matchers import Equals

import tests


class ArchitectureTestCase(tests.unit.TestCase):

    scenarios = [
        ('lists', {
            'architectures': {'build-on': ['amd64'], 'run-on': ['amd64']},
            'expected_build_on': ['amd64'],
            'expected_run_on': ['amd64'],
            'expected_build_error': None,
        }),
        ('strings', {
            'architectures': {'build-on': 'amd64', 'run-on': 'amd64'},
            'expected_build_on': ['amd64'],
            'expected_run_on': ['amd64'],
            'expected_build_error': None,
        }),
        ('no run-on', {
            'architectures': {'build-on': ['amd64']},
            'expected_build_on': ['amd64'],
            'expected_run_on': ['amd64'],
            'expected_build_error': None,
        }),
        ('not required', {
            'architectures': {
                'build-on': ['amd64'],
                'run-on': 'amd64',
                'build-error': 'ignore'},
            'expected_build_on': ['amd64'],
            'expected_run_on': ['amd64'],
            'expected_build_error': 'ignore',
        }),
    ]

    def test_architecture(self):
        architecture = Architecture.from_dict(self.architectures)
        self.assertThat(architecture.build_on, Equals(self.expected_build_on))
        self.assertThat(architecture.run_on, Equals(self.expected_run_on))
        self.assertThat(
            architecture.build_error, Equals(self.expected_build_error))


class ArchitectureErrorTestCase(tests.unit.TestCase):

    def test_missing_build_on_raises(self):
        raised = self.assertRaises(
            errors.MissingPropertyError, Architecture.from_dict,
            {'run-on': 'amd64'})

        self.assertThat(raised.property, Equals('build-on'))
