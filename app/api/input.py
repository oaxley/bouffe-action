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
# @brief	Interface for sending read input to backend
#----- imports

import app.config as config
from . import api, create_response
from flask import abort


from .entity import E, EntityType, get_one_entity_raw
from .scale import get_stable_scale_reading

import time
from datetime import datetime

COMMANDS = {
    'DUMMY' : None
}

RECORDS = []

current_provider = ""

def process_command(command):
    return create_response(f"Executed {command}",
            config.HTTP_OK)

def set_provider(provider):
    global current_provider
    provider_name = E[provider]['name']
    current_provider = provider

    return create_response(f"Setting current provider to {provider} / {provider_name} ",
            config.HTTP_OK)

def record_input(product):
    if not current_provider:
        return abort(config.HTTP_BAD_REQUEST, "Please scan a provider first")
    weight = get_stable_scale_reading()
    now = datetime.now()
    RECORDS.append((product, current_provider, weight, now))
    print(RECORDS)

    return create_response(f"Add {weight} kg for {product}",
            config.HTTP_OK)

def barcode(barcode):
    """Process the ping-pong request"""

    if barcode in COMMANDS:
        process_command(barcode)
    elif barcode in E:
        # we're either scanning a provider (i.e setting the current one)
        # or scanning a product (i.e we need the scale reading)
        entity = E[barcode]
        if entity['etype'] == EntityType.PRODUCT:
            return record_input(barcode)
        elif entity['etype'] == EntityType.PROVIDER:
            return set_provider(barcode)
    else:
        abort(config.HTTP_NOT_FOUND, "The entity {} doesn't exists")



def get_input():
    res = []

    for r in RECORDS:
        (product, provider, weight, ts) = r
        p = get_one_entity_raw(product)
        f = get_one_entity_raw(provider)
        res.append({'provider': f['name'], 'product': p['name'], 'weigth': weight, 'ts':ts})
    print(res)
    return create_response( res, config.HTTP_OK)
