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
# @brief	Interface for interacting with providers
#----- imports

import app.config as config
from . import api, create_response
from flask import abort

FOURNISSEURS = [
    { "id": "F00001", "name":"Provigo" , "address": "xxx" },
    { "id": "F00002", "name":"IPA"  , "address": "yyy"},
    { "id": "F00003", "name":"Metro"  , "address": "zzz"},
]

F = { f['id'] : f for f in FOURNISSEURS}

#----- functions
def get_providers():
    """Process the ping-pong request"""
    return create_response(
        list(F.items()),
        config.HTTP_OK
    )


def get_one_provider(fid):
    """Process the ping-pong request"""
    if fid in F:
        return create_response(
            F[fid],
            config.HTTP_OK)
    else:
        abort(406, "Le Fournisseur {} n'existe pas")

def delete_one_provider(fid):
    """Process the ping-pong request"""
    if fid in F:
        fname = F[fid]["name"]
        faddr = F[fid]["address"]
        return create_response(
            f"Le fournisseur {fid}/ {fname} / {faddr} a ete supprime",
            config.HTTP_OK)
    else:
        abort(406, "Le Fournisseur {} n'existe pas")

def update_one_provider(fournisseur):
    create_or_update_provider(fournisseur=fournisseur, update=True)

def create_provider(fournisseur):
    create_or_update_provider(fournisseur=fournisseur, update=False)

def create_or_update_provider(fournisseur, update):
    fid = fournisseur.get("fid")
    fname = fournisseur.get("fname")
    faddress = fournisseur.get("faddress", "")
    if not update and fid in F:
        abort(
            406,
            f"Le fournisseur {fid} : {fname} existe deja"
        )
    elif update and fid not in F:
        abort(
            406,
            f"Le fournisseur {fid} : {fname} n'existe pas"
        )
    else:
        F[fid] = {
            "id": fid,
            "name": fname,
            "address": faddress,
        }

        return F[fid], 201
