# -*- coding: utf-8 -*-
"""
    flask_saml.views
    ~~~~~~~~~~~~~~~~~~~~
    Flask-SAML views module
    :copyright: (c) 2016 by Tony Tan.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint, request
from saml2 import entity

from idp.utils import get_saml_idp


def idp_initiated(idp_name):
    idp_instance = get_saml_idp(idp_name)
    saml_client = idp_instance.saml_client
    authn_response = saml_client.parse_authn_request_response(
        request.form['SAMLResponse'],
        entity.BINDING_HTTP_POST)
    authn_response.get_identity()
    user_info = authn_response.get_subject()
    username = user_info.text

    #user = User(username)
    #session['saml_attributes'] = authn_response.ava
    #login_user(user)
    #url = url_for('user')
    # NOTE:
    #   On a production system, the RelayState MUST be checked
    #   to make sure it doesn't contain dangerous URLs!
    #if 'RelayState' in request.form:
    #    url = request.form['RelayState']
    return "Hello World!"


def create_blueprint(state, import_name):
    """Creates the saml extension blueprint"""

    bp = Blueprint(state.blueprint_name, import_name,
                   url_prefix=state.url_prefix,
                   subdomain=state.subdomain,
                   template_folder='templates')

    return bp
