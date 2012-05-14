#!/usr/bin/env python
import logging

import tornado.ioloop
import tornado.web
import tornado.options

from handlers.urls import urls

config = {
    'debug': True,
    'port': 80,
    'cookie_secret': '',
    'xsrf_cookies': True,
    'login_url': '/auth',
    'static_path': 'static/',
    'static_url_prefix': '/static/',
    'template_path': 'templates/',
    'twitter_consumer_key': '',
    'twitter_consumer_secret': '',
}


def main():
    logging.getLogger().setLevel(logging.DEBUG)
    tornado.options.parse_command_line() 
    application = tornado.web.Application(urls, **config)
    application.listen(config['port'])
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
