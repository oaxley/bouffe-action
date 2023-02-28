# -*- coding: utf-8 -*-
# vim: filetype=python
#
# This source file is subject to the Apache License 2.0
# that is bundled with this package in the file LICENSE.txt.
# It is also available through the Internet at this address:
# https://opensource.org/licenses/Apache-2.0
#
# @author	Sebastien LEGRAND
# @license	Apache License 2.0
#
# @brief	Ping-pong api route for keep-alive testing

#----- imports
from datetime import datetime

import app.config as config
from . import api, create_response


#----- functions
def ping():
    """Process the ping-pong request"""
    return create_response(
        {
            "pong": datetime.utcnow().strftime(config.DATETIME_FORMAT)
        },
        config.HTTP_OK
    )
