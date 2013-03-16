#!/usr/bin/env python
# encoding: utf-8

from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName

from plone.registry import Registry

from collective.socialpublish.controlpanel.interfaces import ISocialPublishControlPanel
# from collective.socialpublish.config import *
from collective.socialpublish.tests import base

DEPENDENCIES = []

class TestInstall(base.BaseTestCase):
    """  """
    def afterSetUp(self):
        pass

    def testQuickInstall(self):
        qi = self.portal.portal_quickinstaller
        self.failUnless('collective.socialpublish' in (p['id'] for p in qi.listInstallableProducts()))
        for d in DEPENDENCIES:
            self.failUnless(d in (p['id'] for p in qi.listInstallableProducts()))
        qi.installProduct('collective.socialpublish')
        self.failUnless(qi.isProductInstalled('collective.socialpublish'))


class TestControlpanel(base.BaseTestCase):
    """ """
    def afterSetUp(self):
        self.loginAsPortalOwner()
        self.registry = Registry()
        self.registry.registerInterface(ISocialPublishControlPanel)
        qi = self.portal.portal_quickinstaller
        qi.installProduct('collective.socialpublish')

    def test_controlpanel_view(self):
        view = getMultiAdapter((self.portal, self.portal.REQUEST),
                               name="socialpublish-settings")
        view = view.__of__(self.portal)
        self.failUnless(view())

    def test_controlpanel_view_protected(self):
        from AccessControl import Unauthorized
        self.logout()
        self.assertRaises(Unauthorized,
                          self.portal.restrictedTraverse,
                          '@@socialpublish-settings')

    def test_in_controlpanel(self):
        self.controlpanel = getToolByName(self.portal, "portal_controlpanel")
        self.failUnless('socialpublish_settings' in [a.getAction(self)['id']
                                      for a in self.controlpanel.listActions()])

    def test_record_content_types(self):
        record_content_types = self.registry.records[
            'collective.socialpublish.controlpanel.interfaces.ISocialPublishControlPanel.content_types']
        self.failUnless('content_types' in ISocialPublishControlPanel)
        self.assertEquals(record_content_types.value, u"")


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    suite.addTest(makeSuite(TestControlpanel))
    return suite
