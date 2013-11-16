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
from Products.statusmessages.interfaces import IStatusMessage

from collective.socialpublish.events import get_page_list
from collective.socialpublish.controlpanel.utils import fb_page_info_list_to_str

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
        portal_messages = IStatusMessage(self.request)
        portal_url = getToolByName(self.context, 'portal_url')()
        here_url = portal_url + "/@@facebook-auth"
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISocialPublishControlPanel)
        fb_app_id = settings.fb_app_id
        fb_app_secret = settings.fb_app_secret

        code = self.request.form.get('code')
        if code is None:
            portal_messages.add(u"Illegal access because nothing 'code'", type=u"error")
            return self.request.RESPONSE.redirect("@@socialpublish-settings")
        token_res = get_resource('/oauth/access_token', {'client_id': fb_app_id,
                                               'redirect_uri': here_url,
                                               'client_secret': fb_app_secret,
                                               'code': code})
        fb_access_token = urlparse.parse_qs(token_res).get('access_token')
        try:
            fb_access_token_unicode = unicode(fb_access_token[0], 'utf-8')
        except IndexError:
            portal_messages.add(u"Couldn't get Facebook token", type=u"error")
            return self.request.RESPONSE.redirect("@@socialpublish-settings")
        settings.fb_access_token = fb_access_token_unicode

        page_info_list = get_page_list(fb_access_token_unicode)
        settings.fb_page_info = fb_page_info_list_to_str(page_info_list)

        portal_messages.add(u"Getting Facebook page information", type=u"info")
        return self.request.RESPONSE.redirect("@@socialpublish-settings")

