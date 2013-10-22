# coding: utf-8

import urllib2
import urllib
import urlparse
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.socialpublish.controlpanel.interfaces import ISocialPublishControlPanel
from Products.Five.browser import BrowserView
#from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName


ENDPOINT = 'graph.facebook.com'

def get_url(path, args=None):
    args = args or {}
    #if ACCESS_TOKEN:
    #    args['access_token'] = ACCESS_TOKEN
    if 'access_token' in args or 'client_secret' in args:
        endpoint = "https://" + ENDPOINT
    else:
        endpoint = "http://" + ENDPOINT
    return endpoint + path + '?' + urllib.urlencode(args)

def get_resource(path, args=None):
    return urllib2.urlopen(get_url(path, args=args)).read()


class FacebookAuth(BrowserView):
    """

    """
    #template = ViewPageTemplateFile('')

    def __call__(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        here_url = portal_url + "/@@facebook-auth"
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISocialPublishControlPanel)
        fb_app_id = settings.fb_app_id
        fb_app_secret = settings.fb_app_secret

        code = self.request.form.get('code')
        if code is None:
            return "NG"
        res = get_resource('/oauth/access_token', {'client_id': fb_app_id,
                                               'redirect_uri': here_url,
                                               'client_secret': fb_app_secret,
                                               'code': code})
        return res
