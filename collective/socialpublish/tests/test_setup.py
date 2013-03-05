#!/usr/bin/env python
# encoding: utf-8

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



def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestInstall))
    return suite
