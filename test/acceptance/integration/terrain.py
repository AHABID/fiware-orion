# -*- coding: utf-8 -*-
"""
# Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U
#
# This file is part of Orion Context Broker.
#
# Orion Context Broker is free software: you can redistribute it and/or
# modify it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Orion Context Broker is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
# General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Orion Context Broker. If not, see http://www.gnu.org/licenses/.
#
# For those usages not covered by this license please contact with
# iot_support at tid dot es
"""

__author__ = 'Jon Calderin Goñi (jon.caldering@gmail.com)'

from lettuce import before, world, after
from integration.tools.general_utils import stop_mock, drop_all_test_databases

@before.all
def before_all():
    world.entities = None
    world.attributes_consult = None
    world.attributes_creation = None
    world.context_elements = None
    world.notify_conditions = None
    world.context_registrations = None
    world.service = None
    world.subservice = None
    world.mock = None
    world.mock_data = None
    world.payloads_count = -1
    world.response_count = -1
    world.cb_count = -1
    world.cb = {}
    world.payloads = {}
    world.responses = {}


@after.each_scenario
def after_each_scenario(scenario):
    stop_mock()
    world.cb[world.cb_count].log = None

@after.all
def after_all(total):
    drop_all_test_databases(world.config['mongo']['host'], int(world.config['mongo']['port']))