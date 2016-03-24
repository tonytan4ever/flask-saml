# -*- coding: utf-8 -*-
"""
    flask_saml.views
    ~~~~~~~~~~~~~~~~~~~~
    Flask-SAML views module
    :copyright: (c) 2016 by Tony Tan.
    :license: MIT, see LICENSE for more details.
"""

try:
    from xml.etree import ElementTree
except ImportError:
    from elementtree import ElementTree

from flask import current_app, request, abort, redirect
from flask_security.decorators import anonymous_user_required
from flask_saml.utils import get_config, get_security_config, get_location

from saml2 import BINDING_HTTP_REDIRECT, BINDING_HTTP_POST
from saml2.client import Saml2Client


@anonymous_user_required
def login():
    """SAML Authorization Request initiator

    This view initiates the SAML2 Authorization handshake
    using the pysaml2 library to create the AuthnRequest.
    It uses the SAML 2.0 Http Redirect protocol binding.
    """
    logger = current_app.logger

    logger.debug('Login process started')

    came_from = request.GET.get('next',
                                get_security_config('POST_LOGIN_VIEW'))


    selected_idp = request.GET.get('idp', None)
    #conf = get_config(config_loader_path, request)

    # is a embedded wayf needed?
    #idps = available_idps(conf)
    #if selected_idp is None and len(idps) > 1:
    #    logger.debug('A discovery process is needed')
    #    return render_to_response(wayf_template, {
    #            'available_idps': idps.items(),
    #            'came_from': came_from,
    #            }, context_instance=RequestContext(request))

    client = Saml2Client(conf)
    try:
        (session_id, result) = client.prepare_for_authenticate(
            entityid=selected_idp, relay_state=came_from,
            binding=BINDING_HTTP_REDIRECT,
            )
    except TypeError, e:
        logger.error('Unable to know which IdP to use')
        abort(unicode(e))

    logger.debug('Saving the session_id in the OutstandingQueries cache')
    #oq_cache = OutstandingQueriesCache(request.session)
    #oq_cache.set(session_id, came_from)

    logger.debug('Redirecting the user to the IdP')
    return redirect(get_location(result))


def register_namespace_prefixes():
    from saml2 import md, saml, samlp
    #import xmlenc
    #import xmldsig
    prefixes = (('saml', saml.NAMESPACE),
                ('samlp', samlp.NAMESPACE),
                ('md', md.NAMESPACE)
                #('ds', xmldsig.NAMESPACE),
                #('xenc', xmlenc.NAMESPACE)
                )
    if hasattr(ElementTree, 'register_namespace'):
        for prefix, namespace in prefixes:
            ElementTree.register_namespace(prefix, namespace)
    else:
        for prefix, namespace in prefixes:
            ElementTree._namespace_map[namespace] = prefix

register_namespace_prefixes()
