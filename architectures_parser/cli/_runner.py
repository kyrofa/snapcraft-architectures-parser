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

import click

import architectures_parser


@click.command()
@click.argument('snapcraft_yaml', type=click.File('r'),
                metavar='<snapcraft.yaml>')
@click.argument('architectures', metavar='<architectures>')
def run(snapcraft_yaml, architectures):
    """Parse snapcraft.yaml architectures according to those supported.

    <snapcraft.yaml> is the path to the snapcraft.yaml to be parsed.
    <architectures> is a comma-separated and prioritized list of supported
    architectures.
    """

    instances = architectures_parser.determine_build_instances(
        snapcraft_yaml.read(), architectures.split(','))
    click.echo([i.__dict__ for i in instances])
