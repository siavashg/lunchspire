import tornado.database

db = tornado.database.Connection('localhost', 'lunchspire', 'user', 'password')
