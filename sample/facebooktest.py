#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import os.path
import sys
import json
import urllib2
import urllib
import urlparse
import BaseHTTPServer
import webbrowser
import ConfigParser

from facebook import GraphAPI
 
ENDPOINT = 'graph.facebook.com'
REDIRECT_URI = 'http://localhost:8080/fb_auth/'
ACCESS_TOKEN = None
LOCAL_FILE = 'fb_access_token'
PAGE_ID = '641223542564630'
 
def get_url(path, args=None):
    args = args or {}
    if ACCESS_TOKEN:
        args['access_token'] = ACCESS_TOKEN
    if 'access_token' in args or 'client_secret' in args:
        endpoint = "https://" + ENDPOINT
    else:
        endpoint = "http://" + ENDPOINT
    return endpoint + path + '?' + urllib.urlencode(args)
 
def get(path, args=None):
    return urllib2.urlopen(get_url(path, args=args)).read()
 
class RequestHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    app_id = None
    app_secret = None
 
    def do_GET(self):
        global ACCESS_TOKEN
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
 
        code = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('code')
        code = code[0] if code else None
        if code is None:
            self.wfile.write("Sorry, authentication failed.")
            sys.exit(1)
        response = get('/oauth/access_token', {'client_id': self.app_id,
                                               'redirect_uri': REDIRECT_URI,
                                               'client_secret': self.app_secret,
                                               'code': code})
        print response
        ACCESS_TOKEN = urlparse.parse_qs(response)['access_token'][0]
        open(LOCAL_FILE,'w').write(ACCESS_TOKEN)
        self.wfile.write("You have successfully logged in to facebook. "
                         "You can close this window now.")

def get_access_token(app_config):
    global ACCESS_TOKEN
    if not os.path.exists(LOCAL_FILE):
        print "Logging you in to facebook..."
        auth_url = get_url('/oauth/authorize',
                      {'client_id': app_config['id'],
                       'redirect_uri':REDIRECT_URI,
                       'scope':'publish_stream,offline_access,manage_pages'})
        print auth_url
        webbrowser.open(auth_url)
 
        RequestHandler.app_id = app_config['id']
        RequestHandler.app_secret = app_config['secret']
        httpd = BaseHTTPServer.HTTPServer(('127.0.0.1', 8080), RequestHandler)
        while ACCESS_TOKEN is None:
            httpd.handle_request()
    else:
        ACCESS_TOKEN = open(LOCAL_FILE).read()

def get_page_dict(graph):
    page_dict = {}

    response = graph.get_connections('me', 'accounts')

    for data in response['data']:
        page_dict[data['id']] = data['access_token']

    return page_dict

def put_message(page_id, page_dict, message):
    access_token = page_dict.get(page_id, None)
    if access_token != None:
        data = {
            'message': message,
            'access_token': access_token,
            'link': 'http://connpass.com/event/3785/',
            }
        graph.put_object(page_id, 'links', **data)
 
if __name__ == '__main__':
    config = ConfigParser.ConfigParser()
    config.read('facebooktest.ini')
    app_config = config._sections['App']

    # アクセストークンを取得
    get_access_token(app_config)

    graph = GraphAPI(ACCESS_TOKEN)

    # Facebook ページのアクセストークンを取得
    page_dict = get_page_dict(graph)

    # 自分の wall にメッセージを書き込み
    data = {
        'message': 'python スクリプトから投稿',
        'link': 'http://connpass.com/event/3785/',
        'privacy': {'value':'SELF'}, # for testing
        }

    graph.put_object('me', 'links', **data)

    # Facebook ページにメッセージを書き込み
    put_message(PAGE_ID, page_dict, 'python スクリプトから投稿')
