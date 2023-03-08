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
# @brief	Interface for interacting with the scale
#----- imports

import app.config as config
from . import api, create_response
from flask import abort
import random
import math
stable = False
value = random.randint(1,90)/10

def get_scale():
    global stable, value
    stable = random.randint(0,10) > 3
    if not stable:
        value *= random.uniform(0.7,1.3)

    return create_response(
        {'value':round(value,2), 'stable': stable},
        config.HTTP_OK
    )