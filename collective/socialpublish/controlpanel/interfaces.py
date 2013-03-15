
from zope import schema
from zope.interface import Interface

from collective.socialpublish import SocialPublishMessageFactory as _


class ISocialPublishControlPanel(Interface):
    """Social Publish setting interface
    """

    content_types = schema.Text(
        required=False,
        title=_(u'content types'),
        description=_(u'Select content types',
                      default=u'Select content type'),
        default=u"",
        )

    workflow_transactions = schema.Text(
        required=False,
        title=_(u'workflow transactions'),
        description=_(u'Select workflow transactionss',
                      default=u'Select workflow transactions'),
        default=u"",
        )

