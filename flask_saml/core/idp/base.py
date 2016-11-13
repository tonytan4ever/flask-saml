'''
Created on Nov 12, 2016

@author: tonytan4ever
'''

from flask import url_for
import requests
from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT
)
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config
from werkzeug import cached_property

from flask_saml.core import settings


class BaseIdentityProvider(object):

    def __init__(self, idp_name):
        if idp_name not in settings["metadata_url_for"]:
            raise Exception("Settings for IDP '{}' not found".
                            format(idp_name))
        self.name = idp_name
        self.metadata_url = settings["metadata_url_for"][self.name]

    @cached_property
    def acs_url(self):
        return url_for(
            "idp_initiated",
            idp_name=self.name,
            _external=True
        )

    @cached_property
    def https_acs_url(self):
        return url_for(
            "idp_initiated",
            idp_name=self.name,
            _external=True,
            _scheme='https'
        )

    @cached_property
    def saml_metadata(self):
        return requests.get(self.metadata_url)

    @cached_property
    def config_settings(self):
        settings = {
            'metadata': {
                'inline': [self.saml_metadata.text],
                },
            'service': {
                'sp': {
                    'endpoints': {
                        'assertion_consumer_service': [
                            (self.acs_url, BINDING_HTTP_REDIRECT),
                            (self.acs_url, BINDING_HTTP_POST),
                            (self.https_acs_url, BINDING_HTTP_REDIRECT),
                            (self.https_acs_url, BINDING_HTTP_POST)
                        ],
                    },
                    # Don't verify that the incoming requests originate from us
                    # via the built-in cache for authn request ids in pysaml2
                    'allow_unsolicited': True,
                    # Don't sign authn requests, since signed requests only
                    # make sense in a situation where you control both the SP
                    # and IdP
                    'authn_requests_signed': False,
                    'logout_requests_signed': True,
                    'want_assertions_signed': True,
                    'want_response_signed': False,
                },
            },
        }
        spConfig = Saml2Config()
        spConfig.load(settings)
        spConfig.allow_unknown_attributes = True
        return spConfig

    @cached_property
    def saml_client(self):
        saml_client = Saml2Client(config=self.config_settings)
        return saml_client
