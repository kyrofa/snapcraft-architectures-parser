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

import fixtures
import testscenarios
import testtools


class TestCase(testscenarios.WithScenarios, testtools.TestCase):

    def setUp(self):
        super(TestCase, self).setUp()
        tempdir = fixtures.TempDir()
        self.useFixture(tempdir)
        working_directory = tempdir.path
        current_dir = os.getcwd()
        self.addCleanup(os.chdir, current_dir)
        os.chdir(working_directory)
