# -*- coding: utf-8 -*-
# vim: filetype=python
#
# This source file is subject to the Apache License 2.0
# that is bundled with this package in the file LICENSE.txt.
# It is also available through the Internet at this address:
# https://opensource.org/licenses/Apache-2.0
#
# @author	Alex Colson
# @license	Apache License 2.0
#
# @brief	Interface for interacting with entities
#----- imports

import app.config as config
from . import api, create_response
from flask import abort

from enum import Enum

class EntityType(Enum):
    PROVIDER="provider"
    PRODUCT="product"


ENTITIES = [
    { "id": "F00001", "name":"Provigo" , "etype": EntityType.PROVIDER },
    { "id": "F00002", "name":"IGA"  , "etype": EntityType.PROVIDER },
    { "id": "F00003", "name":"Metro"  , "etype": EntityType.PROVIDER },
    { "id": "P00001", "name":"Fruit" , "etype": EntityType.PRODUCT  },
    { "id": "P00002", "name":"Bread"  , "etype": EntityType.PRODUCT },
    { "id": "P00003", "name":"Vegetables"  , "etype": EntityType.PRODUCT },
]

E = { f['id'] : f for f in ENTITIES}

#----- functions
def get_entities_by_type(etype):
    """Process the ping-pong request"""
    if etype:
        res = [ r for r in E.values() if r['etype'] == etype ]
    else:
        res = E.values()
    return create_response(
        list(res),
        config.HTTP_OK
    )


def get_entities():
    return get_entities_by_type(etype=None)


def get_one_entity_raw(eid):
    return E[eid]

def get_one_entity(eid):
    """Process the ping-pong request"""
    if eid in E:
        entity = get_one_entity_raw(eid)
        return create_response(
            entity,
            config.HTTP_OK)
    else:
        abort(config.HTTP_NOT_FOUND, "The entity {} doesn't exists")

def delete_one_entity(eid):
    """Process the ping-pong request"""
    if eid in E:
        fname = E[eid]["name"]
        faddr = E[eid]["address"]
        return create_response(
            f"The entity  {eid}/ {fname} / {faddr} has been deleted",
            config.HTTP_OK)
    else:
        abort(config.HTTP_NOT_FOUND, "The entity  {} doesn't exists")

def update_one_entity(entity):
    create_or_update_entity(entity=entity, update=True)

def create_entity(entity):
    create_or_update_entity(entity=entity, update=False)

def create_or_update_entity(entity, update):
    eid = entity.get("eid")
    ename = entity.get("ename")
    etype = entity.get("etype", "")
    if not update and eid in E:
        abort(
            config.HTTP_NOT_FOUND,
            f"The entity {eid} : {ename} already exists"
        )
    elif update and eid not in E:
        abort(
            config.HTTP_NOT_FOUND,
            f"he entity  {eid} : {ename} doesn't exists"
        )
    else:
        E[eid] = {
            "id": eid,
            "name": ename,
            "address": etype,
        }

        return E[eid], config.HTTP_OK
