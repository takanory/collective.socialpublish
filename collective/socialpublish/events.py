#

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.socialpublish.controlpanel.interfaces import ISocialPublishControlPanel

def _dummy_tw_push(*args):
    print args #TODO
    pass

def _dummy_fb_pash(*args):
    print args #TODO
    pass


def social_publish(obj, event):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISocialPublishControlPanel)
    content_types = settings.content_types
    workflow_transitions = settings.workflow_transitions
    if obj.portal_type not in content_types:
        return None
    if event.transition.id not in workflow_transitions:
        return None

    prefix_message = settings.prefix_message
    tw_consumer_key = settings.tw_consumer_key
    tw_consumer_secret = settings.tw_consumer_secret
    tw_access_key = settings.tw_access_key
    tw_access_secret = settings.tw_access_secret
    fb_app_id = settings.fb_app_id
    fb_app_secret = settings.fb_app_secret
    fb_user_id = settings.fb_user_id

    message = prefix_message + obj.title + u" " + obj.absolute_url()
    if tw_consumer_key and tw_consumer_secret and \
            tw_access_key and tw_access_secret:
        _dummy_tw_push(tw_consumer_key, tw_consumer_secret,
                       tw_access_key, tw_access_secret,
                       message)
    if fb_app_id and fb_app_secret and fb_user_id:
        _dummy_fb_pash(fb_app_id, fb_app_secret, fb_user_id,
                       message)
