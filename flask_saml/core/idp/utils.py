# -*- coding: utf-8 -*-
"""
    flask_saml.core.idp.utils
    ~~~~~~~~~~~~~~~~~~~
    Flask-saml core identity provider module
    :copyright: (c) 2012 by Tony Tan.
    :license: MIT, see LICENSE for more details.
"""

from .okta import OktaIdentityProvider


def get_saml_idp(idp_name):
    # A handful of mapping of idp_name and real idp class
    idp_nam_class_mapping = {
        "okata": OktaIdentityProvider


    }
    return idp_nam_class_mapping[idp_name]
