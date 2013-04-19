#!/usr/bin/python2.7

import os.path
import json
import urllib2
import urllib
import urlparse
import BaseHTTPServer
import webbrowser
from facebook import GraphAPI
 
APP_ID = '134080240108023'
APP_SECRET = '28d7a2002acad518b24177887d300593'
ENDPOINT = 'graph.facebook.com'
REDIRECT_URI = 'http://localhost:8080/fb_auth'
ACCESS_TOKEN = None
LOCAL_FILE = 'fb_access_token'
 
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
        response = get('/oauth/access_token', {'client_id': APP_ID,
                                               'redirect_uri': REDIRECT_URI,
                                               'client_secret': APP_SECRET,
                                               'code': code})
        ACCESS_TOKEN = urlparse.parse_qs(response)['access_token'][0]
        open(LOCAL_FILE,'w').write(ACCESS_TOKEN)
        self.wfile.write("You have successfully logged in to facebook. "
                         "You can close this window now.")
 
if __name__ == '__main__':
    if not os.path.exists(LOCAL_FILE):
        print "Logging you in to facebook..."
        webbrowser.open(get_url('/oauth/authorize',
                                {'client_id':APP_ID,
                                 'redirect_uri':REDIRECT_URI,
                                 'scope':'publish_stream,read_stream'}))
 
        httpd = BaseHTTPServer.HTTPServer(('127.0.0.1', 8080), RequestHandler)
        while ACCESS_TOKEN is None:
            httpd.handle_request()
    else:
        ACCESS_TOKEN = open(LOCAL_FILE).read()

    graph = GraphAPI(ACCESS_TOKEN)
    user = graph.get_object("me")
    print user
    friends = graph.get_connections(user["id"], "friends")
    print len(friends)

    graph.put_object("me", "feed", message="Hello, world")
