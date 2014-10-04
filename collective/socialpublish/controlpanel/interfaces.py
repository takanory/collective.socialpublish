
from zope import schema
from zope.interface import Interface
from zope.component import getUtility
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

from collective.socialpublish import SocialPublishMessageFactory as _


FB_PRIVACY_V = SimpleVocabulary(
            [SimpleTerm(value=u"1", token='sunny', title=u'Sunny'),
            SimpleTerm(value=u"2", token='raining', title=u'Raining'),
            SimpleTerm(value=u"3", token='sunny3', title=u'Sunny3')])

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

    # fb_user_id = schema.TextLine(
    #     required=False,
    #     title=_(u"Facebook UserID"),
    #     default=u""
    #     )

    fb_privacy_setting = schema.Choice(
        required=False,
        title=_(u'Facebook privacy setting'),
        default=u"",
        vocabulary = "collective.socialpublish.fb_privacy_settings",
        )

    fb_access_token = schema.TextLine(
        required=False,
        title=_(u"Facebook access token"),
        default=u""
        )

    fb_page_info = schema.Text(
        required=False,
        title=_(u"Facebook Page information"),
        description=u"PageId|PageTitle|Token",
        default= u"",
    )

    fb_push_select = schema.Choice(
        required=False,
        title=_(u'Facebook privacy setting'),
        default=u"",
        vocabulary = "collective.socialpublish.fb_push_select",
        )

    url_for_publish = schema.TextLine(
        required=False,
        title=_(u"Publish URL"),
        description=u"If you use edit URL, not same Publish URL. e.g.) http://www.cmscom.jp",
    )
