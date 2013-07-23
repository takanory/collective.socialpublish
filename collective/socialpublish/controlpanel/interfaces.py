
from zope import schema
from zope.interface import Interface
from zope.component import getUtility

from collective.socialpublish import SocialPublishMessageFactory as _



class ISocialPublishControlPanel(Interface):
    """Social Publish setting interface
    """

    content_types = schema.Set(
        required=False,
        title=_(u'content types'),
        description=_(u'Select content types',
                      default=u'Select content type'),
        default=set(),
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.ReallyUserFriendlyTypes"),
        )

    workflow_transitions = schema.Set(
        required=False,
        title=_(u'workflow transitions'),
        description=_(u'Select workflow transitions',
                      default=u'Select workflow transitions'),
        default=set(),
        value_type=schema.Choice(vocabulary="plone.app.vocabularies.WorkflowTransitions"),

        )



