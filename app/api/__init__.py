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
# @brief	Flask Application routes initializer

#----- imports
from __future__ import annotations
from typing import Dict, List, Any

from importlib import (
    import_module, resources
)

from flask import (
    Blueprint,
    Response, make_response, jsonify
)


#----- functions
def create_response(payload: Dict[str, Any], status_code: int) -> Response:
    """Create a Flask Response object from a payload and a status code

    Args:
        payload: the payload for the Response
        status_code: HTTP status code for the Response

    Returns:
        A Flask Response object
    """
    response = make_response(jsonify(payload), status_code)
    response.headers['Content-Type'] = "application/json"
    return response


#----- begin

# create the blueprint for the API routes
api = Blueprint('api', __name__, url_prefix="/api")

# imports all the routes under this directory automatically
for name in resources.contents(__name__):
    if name.endswith(".py") and (name != "__init__.py"):
        import_module(f"{__name__}.{name[:-3]}")
