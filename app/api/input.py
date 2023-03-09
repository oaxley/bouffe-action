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

def process_input(data) -> Response:
    if ('command' in data) and (data['command'] in COMMANDS):
        return COMMANDS[data['command']](data)


def create_entry(data) -> Response:
    """Create a new entry in the RECORDS array"""

    # retrieve the data from the front-end
    try:
        provider = data['provider']
        product = data['product']
        weight = data['weight']
        now = datetime.now()

        # record the entry
        RECORDS.append(Record(provider, product, weight, now))

        # create the response
        return create_response(now, config.HTTP_OK)

    except KeyError:
        abort(config.HTTP_BAD_REQUEST, "Missing fields.")


def get_entries() -> Response:
    results = []
    for r in RECORDS:
        results.append({
            'provider': r.provider,
            'product': r.product,
            'weight': r.weight,
            'timestamp': r.timestamp
        })

    return create_response({
        'records': results
    }, config.HTTP_OK)


#----- begin

# define the list of available commands
COMMANDS: Dict[str, Callable] = {
    'CREATE': create_entry,
}

# the list of entities for this session
RECORDS: List[Record] = []
