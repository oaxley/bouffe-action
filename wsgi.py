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
# @brief	Main Entry Point

#----- imports
from flask import render_template

import connexion

options = { "static_folder":"./static"}

app = connexion.FlaskApp(__name__, specification_dir="./app/api", server_args=options)

app.add_api("swagger.yml")


@app.route("/")
def index():
    return render_template("index.html", template_folder="static")



if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)