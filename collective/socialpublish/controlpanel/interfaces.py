
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

    prefix_message = schema.TextLine(
        required=False,
        title=_(u"Adding prefix message"),
        default=u"",
        )

    tw_consumer_token = schema.TextLine(
        required=False,
        title=_(u"Twitter CONSUMER_TOKEN"),
        default=u""
        )

    tw_consumer_secret = schema.TextLine(
        required=False,
        title=_(u"Twitter CONSUMER_SECRET"),
        default=u""
        )

    tw_access_token = schema.TextLine(
        required=False,
        title=_(u"Twitter ACCESS_TOKEN"),
        default=u""
        )

    tw_access_secret = schema.TextLine(
        required=False,
        title=_(u"Twitter ACCESS_SECRET"),
        default=u""
        )

    fb_app_id = schema.TextLine(
        required=False,
        title=_(u"Facebook APP_ID"),
        default=u""
        )

    fb_app_secret = schema.TextLine(
        required=False,
        title=_(u"Facebook APP_SECRET"),
        default=u""
        )

    fb_user_id = schema.TextLine(
        required=False,
        title=_(u"Facebook UserID"),
        default=u""
        )
