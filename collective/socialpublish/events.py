#

import urllib
from urlparse import urlparse

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.socialpublish.controlpanel.interfaces import ISocialPublishControlPanel

import tweepy
from facebook import GraphAPI

# Endpointo of Facebook Graph API
ENDPOINT = 'graph.facebook.com'

def tw_push(tw_consumer_token, tw_consumer_secret, tw_access_token,
            tw_access_secret, message, url):
    auth = tweepy.OAuthHandler(tw_consumer_token, tw_consumer_secret)
    auth.set_access_token(tw_access_token, tw_access_secret)
    api = tweepy.API(auth_handler=auth, api_root='/1.1', secure=True)

    api.update_status(message + u" " + url)

def fb_push(fb_app_id, fb_app_secret, fb_user_id, message, url):
    oauth_args = dict(client_id     = fb_app_id,
                      client_secret = fb_app_secret,
                      grant_type    = 'client_credentials')
    oauth_param = urllib.urlencode(oauth_args)
    oauth_url = 'https://' + ENDPOINT + '/oauth/access_token?' + oauth_param
    oauth_response = urllib.urlopen(oauth_url).read()
    _param, access_token = oauth_response.split('=')

    o = urlparse(url)
    if "." not in o.netloc:
        # localhost(e.g. http://localhost:8080) can not use link paramater
        message = message + u" " + url
        data = {
            'message': message.encode('utf-8'),
            'privacy': {'value':'SELF'}, # for testing
            }
    else:
        data = {
            'message': message.encode('utf-8'),
            'link': url,
            'privacy': {'value':'SELF'}, # for testing
            }

    graph = GraphAPI(access_token)
    graph.put_object(fb_user_id, 'feed', **data)

def fb_push(fb_access_token, fb_user_id, message, url):
    """
    Facebook Post to Wall with access_token
    """
    pass

def fb_page_push(fb_access_token, fb_page_id, fb_page_access_token,
                 message, url):
    """
    Facebook Post to Page with access_token
    """
    pass

def get_page_list(fb_access_token):
    graph = GraphAPI(fb_access_token)
    page_list = []

    response = graph.get_connections('me', 'accounts')
    for data in response['data']:
        page_dict = {'id': data['id'],
                     'title': data['title'],
                     'access_token': data['access_token'],
                     }
        page_list.append(page_dict)

    return page_list

def social_publish(obj, event):
    registry = getUtility(IRegistry)
    settings = registry.forInterface(ISocialPublishControlPanel)
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
    fb_app_id = settings.fb_app_id
    fb_app_secret = settings.fb_app_secret
    fb_user_id = settings.fb_user_id

    message = prefix_message + obj.title
    url = obj.absolute_url()
    if tw_consumer_token and tw_consumer_secret and \
            tw_access_token and tw_access_secret:
       tw_push(tw_consumer_token, tw_consumer_secret,
               tw_access_token, tw_access_secret,
               message, url)
    if fb_app_id and fb_app_secret and fb_user_id:
        fb_push(fb_app_id, fb_app_secret, fb_user_id, message, url)
