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
# @brief	Flask HTTP package

#----- imports
from flask import Flask

from .api import api


#----- functions
def create_app() -> Flask:
    """Function to create the flask application"""
    flask_app = Flask(__name__, static_url_path="", static_folder="../../static")
    flask_app.register_blueprint(api)

    # TODO: logging

    return flask_app
