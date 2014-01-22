#

import urllib
from urlparse import urlparse

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.socialpublish.controlpanel.interfaces import ISocialPublishControlPanel

import tweepy
from facebook import GraphAPI

from collective.socialpublish.controlpanel.utils import get_fb_page_token

# Endpointo of Facebook Graph API
ENDPOINT = 'graph.facebook.com'

def tw_push(tw_consumer_token, tw_consumer_secret, tw_access_token,
            tw_access_secret, message, url):
    auth = tweepy.OAuthHandler(tw_consumer_token, tw_consumer_secret)
    auth.set_access_token(tw_access_token, tw_access_secret)
    api = tweepy.API(auth_handler=auth, api_root='/1.1', secure=True)

    api.update_status(message + u" " + url)

def fb_push(fb_access_token, fb_privacy_setting, message, url):

    """
    Post to User's wall with access_token
    """
    graph = GraphAPI(fb_access_token)
    post_data = create_fb_post_data(message=message,
                                    privacy=fb_privacy_setting,
                                    url=url)
    graph.put_object('me', 'feed', **post_data)

def fb_page_push(fb_access_token, fb_page_id, fb_page_access_token,
                 fb_privacy_setting, message, url):
    """
    Post to Facebook Pages with access_token
    """
    graph = GraphAPI(fb_access_token)
    post_data = create_fb_post_data(message=message,
                                    url=url,
                                    access_token=fb_page_access_token)
    if post_data.has_key('link'):
        graph.put_object(fb_page_id, 'links', **post_data)
    else:
        graph.put_object(fb_page_id, 'feed', **post_data)

def create_fb_post_data(message, privacy=None, url=None, access_token=None):
    """
    Create post data dictionary for Facebook wall or page
    """
    post_data = {}

    # set privacy parameter
    # https://developers.facebook.com/docs/reference/api/privacy-parameter/
    if privacy:
        post_data['privacy'] = {'value': privacy}

    if url != None:
        o = urlparse(url)
        if "." not in o.netloc:
            # localhost(e.g. http://localhost:8080) can not use link paramater
            message = message + u" " + url
        else:
            post_data['link'] = url

    # set page access_token
    if access_token:
        post_data['access_token'] = access_token

    post_data['message'] = message.encode('utf-8')
    return post_data

def get_page_list(fb_access_token):
    graph = GraphAPI(fb_access_token)
    page_list = []

    response = graph.get_connections('me', 'accounts')
    for data in response['data']:
        page_dict = {'id': data['id'],
                     'name': data['name'],
                     'access_token': data['access_token'],
                     }
        page_list.append(page_dict)

    return page_list

def social_publish(obj, event):
    registry = getUtility(IRegistry)
    try:
        settings = registry.forInterface(ISocialPublishControlPanel)
    except KeyError:
        return None
    content_types = settings.content_types
    workflow_transitions = settings.workflow_transitions
    if obj.portal_type not in content_types:
        return None
    if event.transition == None:
        return None
    if event.transition.id not in workflow_transitions:
        return None

    prefix_message = settings.prefix_message
    tw_consumer_token = settings.tw_consumer_token
    tw_consumer_secret = settings.tw_consumer_secret
    tw_access_token = settings.tw_access_token
    tw_access_secret = settings.tw_access_secret
    fb_access_token = settings.fb_access_token
    fb_app_id = settings.fb_app_id
    fb_app_secret = settings.fb_app_secret
    fb_user_id = settings.fb_user_id
    fb_privacy_setting = settings.fb_privacy_setting
    fb_push_select = settings.fb_push_select

    if prefix_message is None:
        message = obj.title
    else:
        message = prefix_message + obj.title
    url = obj.absolute_url()
    if tw_consumer_token and tw_consumer_secret and \
            tw_access_token and tw_access_secret:
       tw_push(tw_consumer_token, tw_consumer_secret,
               tw_access_token, tw_access_secret,
               message, url)
    if fb_push_select == 'MY_WALL':
        # User's wall post
        fb_push(fb_access_token, fb_privacy_setting, message, url)
    else:
        #fb_page_info = settings.fb_page_info
        fb_page_id = fb_push_select
        fb_page_access_token = get_fb_page_token(settings, fb_push_select)
        # Page post
        fb_page_push(fb_access_token, fb_page_id, fb_page_access_token,
                     fb_privacy_setting, message, url)
