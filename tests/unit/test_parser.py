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


import architectures_parser

from testtools.matchers import Contains, Equals, HasLength

import tests


class ParserTestCase(tests.unit.TestCase):

    # Scenarios taken from the architectures document:
    # https://forum.snapcraft.io/t/architectures/4972
    scenarios = [
        ('none', {
            'architectures': None,
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected': [
                {'architecture': 'amd64', 'required': True},
                {'architecture': 'i386', 'required': True},
                {'architecture': 'armhf', 'required': True},
            ]
        }),
        ('i386', {
            'architectures': [
                {'build-on': 'i386', 'run-on': ['amd64', 'i386']},
            ],
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected': [
                {'architecture': 'i386', 'required': True},
            ]
        }),
        ('amd64', {
            'architectures': [
                {'build-on': 'amd64', 'run-on': 'all'},
            ],
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected': [
                {'architecture': 'amd64', 'required': True},
            ]
        }),
        ('amd64 and i386', {
            'architectures': [
                {'build-on': 'amd64', 'run-on': 'amd64'},
                {'build-on': 'i386', 'run-on': 'i386'},
            ],
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected': [
                {'architecture': 'amd64', 'required': True},
                {'architecture': 'i386', 'required': True},
            ]
        }),
        ('amd64 and i386 shorthand', {
            'architectures': [
                {'build-on': 'amd64'},
                {'build-on': 'i386'},
            ],
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected': [
                {'architecture': 'amd64', 'required': True},
                {'architecture': 'i386', 'required': True},
            ]
        }),
        ('amd64, i386, and armhf', {
            'architectures': [
                {'build-on': 'amd64', 'run-on': 'amd64'},
                {'build-on': 'i386', 'run-on': 'i386'},
                {
                    'build-on': 'armhf',
                    'run-on': 'armhf',
                    'build-error': 'ignore'
                },
            ],
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected': [
                {'architecture': 'amd64', 'required': True},
                {'architecture': 'i386', 'required': True},
                {'architecture': 'armhf', 'required': False},
            ]
        }),
        ('amd64 priority', {
            'architectures': [
                {'build-on': ['amd64', 'i386'], 'run-on': 'all'},
            ],
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected': [
                {'architecture': 'amd64', 'required': True},
            ]
        }),
        ('i386 priority', {
            'architectures': [
                {'build-on': ['amd64', 'i386'], 'run-on': 'all'},
            ],
            'supported_architectures': ['i386', 'amd64', 'armhf'],
            'expected': [
                {'architecture': 'i386', 'required': True},
            ]
        }),
        ('old style i386 priority', {
            'architectures': ['amd64', 'i386'],
            'supported_architectures': ['i386', 'amd64', 'armhf'],
            'expected': [
                {'architecture': 'i386', 'required': True},
            ]
        }),
        ('old style amd64 priority', {
            'architectures': ['amd64', 'i386'],
            'supported_architectures': ['amd64', 'i386', 'armhf'],
            'expected': [
                {'architecture': 'amd64', 'required': True},
            ]
        }),
    ]

    def setUp(self):
        super(ParserTestCase, self).setUp()

        snapcraft_yaml = tests.SnapcraftYaml(architectures=self.architectures)
        self.useFixture(snapcraft_yaml)
        self.path = snapcraft_yaml.path

    def test_parser(self):
        with open(self.path, 'r') as f:
            build_instances = architectures_parser.determine_build_instances(
                f.read(), self.supported_architectures)
        self.assertThat(build_instances, HasLength(len(self.expected)))
        for instance in build_instances:
            self.assertThat(self.expected, Contains(instance.__dict__))
