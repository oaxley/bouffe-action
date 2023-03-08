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
from app.main.views import main
import connexion

app = connexion.FlaskApp(__name__, specification_dir="./app/api")
app.app.register_blueprint(main, url_prefix="/")
app.add_api("swagger.yml")

if __name__ == "__main__":

    app.run(host="0.0.0.0", port=5000, debug=True)