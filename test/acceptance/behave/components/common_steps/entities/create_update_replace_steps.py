# -*- coding: utf-8 -*-
"""
 Copyright 2015 Telefonica Investigacion y Desarrollo, S.A.U

 This file is part of Orion Context Broker.

 Orion Context Broker is free software: you can redistribute it and/or
 modify it under the terms of the GNU Affero General Public License as
 published by the Free Software Foundation, either version 3 of the
 License, or (at your option) any later version.

 Orion Context Broker is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Affero
 General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with Orion Context Broker. If not, see http://www.gnu.org/licenses/.

 For those usages not covered by this license please contact with
 iot_support at tid dot es
"""
__author__ = 'Iván Arias León (ivan dot ariasleon at telefonica dot com)'

import behave
from behave import step

from iotqatools.helpers_utils import *
from iotqatools.cb_v2_utils import CB
from iotqatools.mongo_utils import Mongo

from tools.properties_config import Properties  # methods in properties class
from tools.NGSI_v2 import NGSI


# constants
CONTEXT_BROKER_ENV = u'context_broker_env'
MONGO_ENV = u'mongo_env'

properties_class = Properties()
props_mongo = properties_class.read_properties()[MONGO_ENV]  # mongo properties dict

# ------------- general_operations.feature -----------------------------------------
behave.use_step_matcher("re")
__logger__ = logging.getLogger("steps")


# ------------------ create_entities ------------------------------------------------

@step(u'a definition of headers')
def service_and_service_path(context):
    """
    configuration of service an service path in headers
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
    """
    props = properties_class.read_properties()[CONTEXT_BROKER_ENV]
    context.cb = CB(protocol=props["CB_PROTOCOL"], host=props["CB_HOST"], port=props["CB_PORT"])
    context.cb.definition_headers(context)


@step(u'create "([^"]*)" entities with "([^"]*)" attributes')
def create_entities_with_properties(context, entities_number, attributes_number):
    """
    create N entities with N attributes and another optional parameters:
        -  entity_type, entity_id, attributes_name, attributes_value, attribute_type, metadata_name and metadata_value
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
    :param entities_number: number of entities
    :param attributes_number: number of attributes
    """
    __logger__.debug("Creating %s with %s attributes..." % (entities_number, attributes_number))
    context.resp_list = context.cb.create_entities(context, entities_number, attributes_number)
    __logger__.info("...Created %s with %s attributes" % (entities_number, attributes_number))


@step(u'create an entity and attribute with special values in raw')
def create_an_entity_and_attribute_with_special_values(context):
    """
    create an entity and attribute with special values in raw
       ex:
             "value": true
             "value": false
             "value": 34
             "value": 5.00002
             "value": [ "json", "vector", "of", 6, "strings", "and", 2, "integers" ]
             "value": {"x": {"x1": "a","x2": "b"}}
             "value": "41.3763726, 2.1864475,14"  -->  "type": "geo:point"
             "value": "2017-06-17T07:21:24.238Z"  -->  "type: "date"
        Some cases are not parsed correctly to dict in python
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
      """
    global cb, resp
    __logger__.debug("Creating an entity with attributes in raw mode...")
    context.resp = context.cb.create_entity_raw(context)
    __logger__.info("...Created an entity with attributes in raw mode")

# ------------------------ update, append and replace -----------------------------------------------


@step(u'update or append attributes by ID "([^"]*)"')
def update_or_append_an_attribute_by_id(context, entity_id):
    """
    update or append attributes by ID
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
    :param entity_id: entity ID
    """
    __logger__.debug("updating or appending an attribute by id...")
    context.resp = context.cb.update_or_append_an_attribute_by_id("POST", context, entity_id)
    __logger__.info("...updated or appended an attribute by id")


@step(u'update or append attributes by ID "([^"]*)" in raw mode')
def update_or_append_an_attribute_by_ID_in_raw_mode(context, entity_id):
    """
    update or append attributes by ID in raw mode
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
    :param entity_id: entity ID
    """
    __logger__.debug("updating or appending an attribute by id in raw mode...")
    context.resp = context.cb.update_or_append_an_attribute_in_raw_by_id("POST", context, entity_id)
    __logger__.info("...updated or appended an attribute by id in raw mode")


@step(u'update an attribute by ID "([^"]*)" if it exists')
def update_an_attribute_by_ID_if_it_exists(context, entity_id):
    """
    update an attribute by ID if it exists
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
    :param entity_id: entity ID
    """
    __logger__.debug("updating or appending an attribute by id if it exists...")
    context.resp = context.cb.update_or_append_an_attribute_by_id("PATCH", context, entity_id)
    __logger__.info("...updated or appended an attribute by id if it exists")


@step(u'update an attribute by ID "([^"]*)" if it exists in raw mode')
def update_an_attribute_by_ID_if_it_exists_in_raw_mode(context, entity_id):
    """
    update or append attributes by ID in raw mode
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
    :param entity_id: entity ID
    """
    __logger__.debug("updating or appending an attribute by id in raw mode if it exists...")
    context.resp = context.cb.update_or_append_an_attribute_in_raw_by_id("PATCH", context, entity_id)
    __logger__.info("...updated or appended an attribute by id in raw mode if it exists")


@step(u'replace attributes by ID "([^"]*)"')
def replace_attributes_by_id(context, entity_id):
    """
    replace attributes by ID
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
    :param entity_id: entity ID
    """
    __logger__.debug("replacing attributes by id...")
    context.resp = context.cb.update_or_append_an_attribute_by_id("PUT", context, entity_id)
    __logger__.info("...replaced attributes by id")


@step(u'replace attributes by ID "([^"]*)" in raw mode')
def replace_attributes_by_idin_raw_mode(context, entity_id):
    """
    replace attributes by ID
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
    :param entity_id: entity ID
    """
    __logger__.debug("replacing attributes by id in raw mode...")
    context.resp = context.cb.update_or_append_an_attribute_in_raw_by_id("PUT", context, entity_id)
    __logger__.info("...replaced attributes by id in raw mode")

# ------------------------------------- validations ----------------------------------------------

@step(u'verify that entities are stored in default tenant at mongo')
@step(u'verify that entities are stored in mongo')
def entities_are_stored_in_mongo(context):
    """
    verify that entities are stored in mongo
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
    """
    __logger__.debug(" >> verifying entities are stored in mongo")
    mongo = Mongo(host=props_mongo["MONGO_HOST"], port=props_mongo["MONGO_PORT"], user=props_mongo["MONGO_USER"],
              password=props_mongo["MONGO_PASS"])
    ngsi = NGSI()
    ngsi.verify_entities_stored_in_mongo(mongo, context.cb.get_entity_context(), context.cb.get_headers())
    __logger__.info(" >> verified entities are stored in mongo")


@step(u'verify that entities are not stored in mongo')
def entities_are_not_stored_in_mongo(context):
    """
    verify that entities are not stored in mongo
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
    """
    __logger__.debug(" >> verifying entities are not stored in mongo")
    mongo = Mongo(host=props_mongo["MONGO_HOST"], port=props_mongo["MONGO_PORT"], user=props_mongo["MONGO_USER"],
              password=props_mongo["MONGO_PASS"])
    ngsi = NGSI()
    ngsi.verify_entities_stored_in_mongo(mongo, context.cb.get_entity_context(), context.cb.get_headers(), False)
    __logger__.info(" >> verified entities are not stored in mongo")


@step(u'verify that an entity is updated in mongo')
def verify_that_an_entity_is_updated_in_mongo(context):
    """
    verify that an entity is updated in mongo
    :param context: It’s a clever place where you and behave can store information to share around. It runs at three levels, automatically managed by behave.
    """
    __logger__.debug(" >> verifying that an entity is updating in mongo")
    mongo = Mongo(host=props_mongo["MONGO_HOST"], port=props_mongo["MONGO_PORT"], user=props_mongo["MONGO_USER"],
              password=props_mongo["MONGO_PASS"])
    ngsi = NGSI()
    ngsi.verify_entity_updated_in_mongo(mongo, context.cb.get_entity_context(), context.cb.get_headers())
    __logger__.info(" >> verified that an entity is updated in mongo")
