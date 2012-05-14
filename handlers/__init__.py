from tornado.web import RequestHandler

from model.user import User

class BaseHandler(RequestHandler):

    def get_current_user(self):
        user_id = self.get_secure_cookie('soup')
        if not user_id:
            return None
        return User.get(user_id)

    def set_login(self, user):
        if not user:
            raise ValueError('Invalid user')
        self.set_secure_cookie('soup', str(user.id))

    def render(self, template_name, **kwargs):

        params = kwargs
        params['user'] = self.current_user
        params['xsrf'] = self.xsrf_form_html()
        return super(BaseHandler, self).render(template_name,
                                               **params)
