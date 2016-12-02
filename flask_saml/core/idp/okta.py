# -*- coding: utf-8 -*-
"""
    flask_saml.core.idp
    ~~~~~~~~~~~~~~~~~~~
    Flask-saml core identity provider module
    :copyright: (c) 2012 by Tony Tan.
    :license: MIT, see LICENSE for more details.
"""


class OktaIdentityProvider(object):

    @property
    def name(self):
        return "Okata"
