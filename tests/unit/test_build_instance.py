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


from architectures_parser import BuildInstance
from architectures_parser._architecture import Architecture
from architectures_parser import errors

from testtools.matchers import Equals

import tests


class BuildInstanceTestCase(tests.unit.TestCase):

    # Single-item scenarios taken from the architectures document:
    # https://forum.snapcraft.io/t/architectures/4972
    scenarios = [
        ('i386', {
            'architecture': Architecture(
                build_on='i386', run_on=['amd64', 'i386']),
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected_architecture': 'i386',
            'expected_required': True,
        }),
        ('amd64', {
            'architecture': Architecture(build_on='amd64', run_on='all'),
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected_architecture': 'amd64',
            'expected_required': True,
        }),
        ('amd64 priority', {
            'architecture': Architecture(
                build_on=['amd64', 'i386'], run_on='all'),
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected_architecture': 'amd64',
            'expected_required': True,
        }),
        ('i386 priority', {
            'architecture': Architecture(
                build_on=['amd64', 'i386'], run_on='all'),
            'supported_architectures': ['i386', 'amd64', 'armhf'],
            'expected_architecture': 'i386',
            'expected_required': True,
        }),
        ('optional', {
            'architecture': Architecture(
                build_on='amd64', build_error='ignore'),
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected_architecture': 'amd64',
            'expected_required': False,
        }),
    ]

    def test_build_instance(self):
        instance = BuildInstance(
            self.architecture, self.supported_architectures)
        self.assertThat(
            instance.architecture, Equals(self.expected_architecture))
        self.assertThat(
            instance.required, Equals(self.expected_required))


class BuildInstanceErrorTestCase(tests.unit.TestCase):

    def test_no_matching_arch_raises(self):
        architecture = Architecture(build_on='amd64', run_on='amd64')
        raised = self.assertRaises(
            errors.UnsupportedBuildOnError, BuildInstance, architecture,
            ['i386'])
        self.assertThat(raised.build_on, Equals(['amd64']))
