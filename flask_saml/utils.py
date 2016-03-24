# -*- coding: utf-8 -*-
"""
    flask_saml.utils
    ~~~~~~~~~~~~~~~~~~~~
    Flask-SAML utils module
    :copyright: (c) 2016 by Tony Tan.
    :license: MIT, see LICENSE for more details.
"""

from flask import current_app


def get_config(app):
    """Conveniently get the security configuration for the specified
    application without the annoying 'SAML_' prefix.
    :param app: The flask application to inspect
    """
    items = app.config.items()
    prefix = 'SAML_'

    def strip_prefix(tup):
        return (tup[0].replace('SAML_', ''), tup[1])

    return dict([strip_prefix(i) for i in items if i[0].startswith(prefix)])


def get_security_config(app):
    """Conveniently get the security configuration for the specified
    application without the annoying 'SECURITY_' prefix. This is for
    flask-security's configurations
    :param app: The flask application to inspect
    """
    items = app.config.items()
    prefix = 'SECURITY_'

    def strip_prefix(tup):
        return (tup[0].replace('SECURITY_', ''), tup[1])

    return dict([strip_prefix(i) for i in items if i[0].startswith(prefix)])


def config_value(key, app=None, default=None):
    """Get a Flask-Security configuration value.
    :param key: The configuration key without the prefix `SECURITY_/SAML_`
    :param app: An optional specific application to inspect. Defaults to
                Flask's `current_app`
    :param default: An optional default value if the value is not set
    """
    app = app or current_app
    return get_config(app).get(key.upper(), default)


def get_location(http_info):
    """Extract the redirect URL from a pysaml2 http_info object"""
    assert 'headers' in http_info
    headers = http_info['headers']

    assert len(headers) == 1
    header_name, header_value = headers[0]
    assert header_name == 'Location'
    return header_value
