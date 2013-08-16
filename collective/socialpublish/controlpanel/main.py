from Acquisition import aq_inner
from plone.app.registry.browser import controlpanel
from zope.component import getMultiAdapter
from Products.Five.browser import BrowserView
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from collective.socialpublish.controlpanel.interfaces import ISocialPublishControlPanel
from collective.socialpublish import SocialPublishMessageFactory as _


class SocialPublishEditForm(controlpanel.RegistryEditForm):

    schema = ISocialPublishControlPanel
    label = _(u"SocialPublish settings")

    def updateFields(self):
        super(SocialPublishEditForm, self).updateFields()

    def updateWidgets(self):
        super(SocialPublishEditForm, self).updateWidgets()
        self.widgets['prefix_message'].addClass('long-input-text')


class SocialPublishControlPanel(controlpanel.ControlPanelFormWrapper):
    form = SocialPublishEditForm



