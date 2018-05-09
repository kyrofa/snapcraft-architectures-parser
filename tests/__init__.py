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

import os
import yaml

import fixtures


class SnapcraftYaml(fixtures.Fixture):

    def __init__(
            self, name='test-snap', version='test-version',
            summary='test-summary', description='test-description',
            confinement='strict', grade='devel', architectures=None):
        super(SnapcraftYaml, self).__init__()

        self.path = os.path.join(os.getcwd(), 'snap', 'snapcraft.yaml')

        self.data = {
            'name': name,
            'confinement': confinement,
            'grade': grade,
            'parts': {},
            'apps': {}
        }
        if architectures is not None:
            self.data['architectures'] = architectures

    def update_part(self, name, data):
        part = {name: data}
        self.data['parts'].update(part)

    def update_app(self, name, data):
        app = {name: data}
        self.data['apps'].update(app)

    def _setUp(self):
        super(SnapcraftYaml, self)._setUp()

        os.makedirs(os.path.dirname(self.path))
        with open(self.path, 'w') as y:
            yaml.dump(self.data, y)
