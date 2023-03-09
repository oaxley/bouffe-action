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
from __future__ import annotations
from typing import Dict, List, Callable

from flask import abort, Response
from datetime import datetime
from dataclasses import dataclass

import app.config as config
from . import create_response


#----- classes
@dataclass
class Record:
    provider: str
    product: str
    weight: str
    timestamp: datetime


#----- functions
def create_entry(data) -> Response:
    """Create a new entry in the RECORDS array"""

    # retrieve the data from the front-end
    try:
        provider = data['provider']
        product = data['product']
        weight = data['weight']
        now = datetime.now()

        # record the entry
        record = Record(provider, product, weight, now)
        RECORDS[id(record)] = record

        # create the response
        return create_response({'id': id(record)}, config.HTTP_OK)

    except KeyError:
        abort(config.HTTP_BAD_REQUEST, "Missing fields.")


def get_entries() -> Response:
    """Return the list of entries in the record"""
    results = []
    for k, v in RECORDS.items():
        results.append({
            'id': k,
            'provider': v.provider,
            'product': v.product,
            'weight': v.weight,
            'timestamp': v.timestamp
        })

    return create_response({
        'records': results
    }, config.HTTP_OK)

def delete_entry(rid) -> Response:
    """Remove an entry from the Records"""
    if int(rid) not in RECORDS:
        abort(config.HTTP_NOT_FOUND, f"Unkown record ID {rid}")
    else:
        del(RECORDS[int(rid)])
        return create_response("", config.HTTP_OK)


#----- begin

# the list of entities for this session
RECORDS: Dict[int, Record] = {}
