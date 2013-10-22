from Acquisition import aq_inner
from plone.app.registry.browser import controlpanel
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName

from collective.socialpublish.controlpanel.interfaces import ISocialPublishControlPanel
from collective.socialpublish import SocialPublishMessageFactory as _

FB_OAUTH_URL =  " https://graph.facebook.com/oauth/authorize"

class SocialPublishEditForm(controlpanel.RegistryEditForm):

    schema = ISocialPublishControlPanel
    label = _(u"SocialPublish settings")

    def updateFields(self):
        super(SocialPublishEditForm, self).updateFields()

    def updateWidgets(self):
        super(SocialPublishEditForm, self).updateWidgets()
        self.widgets['prefix_message'].addClass('long-input-text')

    @property
    def description(self):
        portal_url = getToolByName(self.context, 'portal_url')()
        here_url = portal_url + "/@@facebook-auth"
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ISocialPublishControlPanel)
        fb_app_id = settings.fb_app_id
        fb_app_secret = settings.fb_app_secret
        if fb_app_id and fb_app_secret:
            url = FB_OAUTH_URL + "?client_id=" + fb_app_id + "&redirect_uri=" +\
                    here_url + "&scope=publish_stream"
            print url
            return _(u'''If you did NOT get facebook auth,
                you need to click the link: <a href="%s">Facebook Auth</a>''' % (url,))
        else:
            return _(u'''You need to input fb_app_id and fb_app_secret''')


class SocialPublishControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SocialPublishEditForm




