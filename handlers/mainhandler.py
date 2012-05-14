from handlers import BaseHandler


class MainHandler(BaseHandler):

    def get(self):
        #if not self.current_user:
        #    import logging
        #    logging.error(self.current_user)
        #    return self.render("auth.html")
        self.redirect('/lunches')
