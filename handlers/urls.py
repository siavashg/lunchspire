from handlers.lunchhandler import LunchHandler
from handlers.lunchhandler import LunchCreateHandler
from handlers.lunchhandler import LunchListHandler
from handlers.lunchhandler import LunchJoinHandler
from handlers.mainhandler import MainHandler
from handlers.authhandler import TwitterAuthHandler

urls = [
    (r'/', MainHandler),
    (r'/auth', TwitterAuthHandler),
    (r'/lunch/create', LunchCreateHandler),
    (r'/lunch/([0-9]+)', LunchHandler),
    (r'/lunch/join/([0-9]+)', LunchJoinHandler),
    (r'/lunches', LunchListHandler),
    (r'/lunches/([0-9]+)?', LunchListHandler),
]
