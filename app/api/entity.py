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
from __future__ import annotations

from flask import abort, Response
from dataclasses import dataclass

from . import api, create_response
import app.config as config


#----- globals

# list of entities (will be loaded from XLS later on)
ENTITIES = {
    #----- Providers
    "F00001": "Bono",
    "F00002": "Costco",
    "F00003": "Fraichement Bon",
    "F00004": "IGA",
    "F00005": "Metro",
    "F00006": "Provigo",
    "F00007": "Premiere Moisson",
    "F00008": "Rachelle Bery",
    "F00009": "Jardin Vertical",
    "F00010": "Mamie Clafoutis",

    #----- Products
    "P00001": "Fruits",
    "P00002": "Viennoiseries",
    "P00003": "Legumes",
    "P00004": "Pain",
    "P00005": "Viande",
    "P00006": "Poisson",
    "P00007": "Oeufs",
}


#----- classes
@dataclass
class EntityType:
    name: str
    marker: str

class Entity:
    provider = EntityType("provider", "F")
    product = EntityType("product", "P")

    @staticmethod
    def is_provider(eid: str) -> bool:
        """Return True if the entity ID is a Provider"""
        return eid[0].upper() == Entity.provider.marker

    @staticmethod
    def is_product(eid: str) -> bool:
        """Return True if the entity ID is a Product"""
        return eid[0].upper() == Entity.product.marker

    @staticmethod
    def getType(eid: str) -> str:
        """Return the type of an entity ID"""
        if Entity.is_provider(eid):
            return Entity.provider.name
        elif Entity.is_product(eid):
            return Entity.product.name
        else:
            return ""


#----- functions
def get_entities_by_type(etype: str) -> Response:
    """Return the list of entities according to their types"""
    values = []
    for k in ENTITIES:
        if (etype.lower() == Entity.provider.name) and Entity.is_provider(k):
            values.append(ENTITIES[k])
        if (etype.lower() == Entity.product.name) and Entity.is_product(k):
            values.append(ENTITIES[k])

    return create_response(
        {"entities": values}, config.HTTP_OK
    )

def get_entities() -> Response:
    """Return the list of all the entities"""
    return create_response(
        {"entities": ENTITIES}, config.HTTP_OK
    )

def get_one_entity(eid: str) -> Response:
    """Return an entity according to its id"""
    if eid not in ENTITIES:
        abort(config.HTTP_NOT_FOUND, f"The entity '{eid}' does not exists")
    else:
        return create_response(
            {
                "ename": ENTITIES[eid],
                "eid": eid,
                "etype": Entity.getType(eid)
            },
            config.HTTP_OK
        )


# def delete_one_entity(eid):
#     """Process the ping-pong request"""
#     if eid in E:
#         fname = E[eid]["name"]
#         faddr = E[eid]["address"]
#         return create_response(
#             f"The entity  {eid}/ {fname} / {faddr} has been deleted",
#             config.HTTP_OK)
#     else:
#         abort(config.HTTP_NOT_FOUND, "The entity  {} doesn't exists")

# def update_one_entity(entity):
#     create_or_update_entity(entity=entity, update=True)

# def create_entity(entity):
#     create_or_update_entity(entity=entity, update=False)

# def create_or_update_entity(entity, update):
#     eid = entity.get("eid")
#     ename = entity.get("ename")
#     etype = entity.get("etype", "")
#     if not update and eid in E:
#         abort(
#             config.HTTP_NOT_FOUND,
#             f"The entity {eid} : {ename} already exists"
#         )
#     elif update and eid not in E:
#         abort(
#             config.HTTP_NOT_FOUND,
#             f"The entity  {eid} : {ename} doesn't exists"
#         )
#     else:
#         E[eid] = {
#             "id": eid,
#             "name": ename,
#             "address": etype,
#         }

#         return E[eid], config.HTTP_OK
