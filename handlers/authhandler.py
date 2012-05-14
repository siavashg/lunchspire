import tornado.auth
from tornado.escape import xhtml_escape

from handlers import BaseHandler
from model.user import User

class TwitterAuthHandler(BaseHandler,
                         tornado.auth.TwitterMixin):

    _OAUTH_REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
    _OAUTH_ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
    _OAUTH_AUTHORIZE_URL = 'https://api.twitter.com/oauth/authorize'
    _OAUTH_AUTHENTICATE_URL = 'https://api.twitter.com/oauth/authenticate'
    _OAUTH_NO_CALLBACKS = False

    @tornado.web.asynchronous
    def get(self):
        if self.get_argument('oauth_token', None):
            self.get_authenticated_user(self.async_callback(self._on_auth))
            return
        self.authorize_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, 'Twitter auth failed')

        instance = User.get(user['id'])
        if not instance:
            access_key = user['access_token']['key']
            access_secret = user['access_token']['secret']
            instance = User.create(user['id'], xhtml_escape(user['name']),
                        user['profile_image_url_https'], access_key,
                        access_secret, user['username'])
        if not instance:
            raise RuntimeError('Uhm.. yeah.. about that..')

        self.set_login(instance)
        self.redirect('/')

