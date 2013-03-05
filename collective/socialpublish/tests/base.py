#!/usr/bin/env python
# encoding: utf-8

from Testing import ZopeTestCase
from Products.Five import zcml
from Products.Five import fiveconfigure
from Products.PloneTestCase import PloneTestCase
from Products.PloneTestCase.layer import onsetup

@onsetup
def setup_product():
    """
    """

    # Load the ZCML configuration for the optilux.policy package.

    fiveconfigure.debug_mode = True
    import collective.socialpublish
    zcml.load_config('configure.zcml', collective.socialpublish)
    fiveconfigure.debug_mode = False

    # We need to tell the testing framework that these products
    # should be available. This can't happen until after we have loaded
    # the ZCML.

    ZopeTestCase.installPackage('collective.socialpublish')

# The order here is important: We first call the (deferred) function which
# installs the products we need for the Optilux package. Then, we let
# PloneTestCase set up this product on installation.

setup_product()

PRODUCTS = []
PloneTestCase.setupPloneSite(products=PRODUCTS)

class BaseTestCase(PloneTestCase.PloneTestCase):
    class Session(dict):
        def set(self, key, value):
            self[key] = value

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.app.REQUEST['SESSION'] = self.Session()
