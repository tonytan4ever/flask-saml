# -*- coding: utf-8 -*-
"""
    flask_saml.core.setings
    ~~~~~~~~~~~~~~~~~~~
    Flask-saml core identity settings module
    :copyright: (c) 2012 by Tony Tan.
    :license: MIT, see LICENSE for more details.
"""

from flask import current_app
from werkzeug.local import LocalProxy

# Convenient references
_security = LocalProxy(lambda: current_app.extensions['saml'])

default_config = {
    "metadata_url_for": {

    }
}
