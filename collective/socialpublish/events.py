#

import urllib

from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from collective.socialpublish.controlpanel.interfaces import ISocialPublishControlPanel

import tweepy
from facebook import GraphAPI

ENDPOINT = 'graph.facebook.com'

def tw_push(tw_consumer_token, tw_consumer_secret, tw_access_token,
            tw_access_secret, message):
    auth = tweepy.OAuthHandler(tw_consumer_token, tw_consumer_secret)
    auth.set_access_token(tw_access_token, tw_access_secret)
    api = tweepy.API(auth_handler=auth, api_root='/1.1', secure=True)

    api.update_status(message)

def fb_push(fb_app_id, fb_app_secret, fb_user_id, message):
    oauth_args = dict(client_id     = fb_app_id,
                      client_secret = fb_app_secret,
                      grant_type    = 'client_credentials')
    oauth_param = urllib.urlencode(oauth_args)
    oauth_url = 'https://' + ENDPOINT + '/oauth/access_token?' + oauth_param
    oauth_response = urllib.urlopen(oauth_url).read()
    _token, access_token = oauth_response.split('=')

    graph = GraphAPI(access_token)
    graph.put_wall_post(message=message)
    #graph.put_object("me", # self wall
    #                 "feed",
    #                 message=message
    #                 privacy={'value':'SELF'},
    #                 )

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
    tw_consumer_token = settings.tw_consumer_token
    tw_consumer_secret = settings.tw_consumer_secret
    tw_access_token = settings.tw_access_token
    tw_access_secret = settings.tw_access_secret
    fb_app_id = settings.fb_app_id
    fb_app_secret = settings.fb_app_secret
    fb_user_id = settings.fb_user_id

    message = prefix_message + obj.title + u" " + obj.absolute_url()
    if tw_consumer_token and tw_consumer_secret and \
            tw_access_token and tw_access_secret:
       tw_push(tw_consumer_token, tw_consumer_secret,
               tw_access_token, tw_access_secret,
               message)
    if fb_app_id and fb_app_secret and fb_user_id:
        fb_push(fb_app_id, fb_app_secret, fb_user_id, message)
