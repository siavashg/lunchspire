import tornado.web
import tornado.auth
from tornado.web import authenticated
from handlers import BaseHandler
from model.lunch import Lunch

class LunchHandler(BaseHandler):

    def get(self, lunch_id):
        instance = Lunch.get(lunch_id)
        if not instance:
            self.redirect('/lunch/create')
        params = {'lunch': instance}
        self.render('lunch.html', **params)

class LunchListHandler(BaseHandler):

    def get(self, page=0):
        instances = Lunch.get_page(0)
        if not instances:
            self.redirect('/lunch/create')
        params = {'lunches': instances}
        self.render('lunch_list.html', **params)

class LunchCreateHandler(BaseHandler,
                         tornado.auth.TwitterMixin):
    @authenticated
    def get(self):
        self.render('create_lunch.html')

    @tornado.web.authenticated
    @tornado.web.asynchronous
    def post(self):
        food = self.get_argument('food')
        place = self.get_argument('place')
        lunch_date = self.get_argument('lunch_date')
        tags = self.get_argument('tags').split(',')
        slots = self.get_argument('slots')

        user = self.current_user
        instance = Lunch.create(food=food, place=place, lunch_date=lunch_date,
                                creator_id=user.id, slots=slots, tags=tags)

        url = "http://lunchspire.com/lunch/%s #lspire" % instance.id
        message = "Let's eat lunch at %s on %s, to talk %s %s"
        message = message % (place, lunch_date, ', '.join(tags), url)

        if len(message) > 140:
            message = "Join me for lunch %s" % url


        access_token= {'key': user.access_key, 'secret': user.access_secret}

        self.twitter_request(
            "/statuses/update",
            post_args={"status": message},
            access_token=access_token,
            callback=self.async_callback(self.finish))
        self.redirect('/lunch/%s' % instance.id)

class LunchJoinHandler(BaseHandler,
		       tornado.auth.TwitterMixin):

    @authenticated
    @tornado.web.asynchronous
    def get(self, lunch_id):
        user = self.current_user
        lunch = Lunch.get(lunch_id)
        lunch.add_participant(user.id)

        participants = lunch.participants

        handles = []
        for participant in participants:
            handles.append(participant.handle)

        url = "http://lunchspire.com/lunch/%s #lspire" % lunch.id
        message = "Joining @%s for lunch %s" % (', @'.join(handles), url)

        if len(message) > 140:
            message = "Joining @%s for lunch %s" % (handles[0], url)

        access_token= {'key': user.access_key, 'secret': user.access_secret}

        self.twitter_request(
            "/statuses/update",
            post_args={"status": message},
            access_token=access_token,
            callback=self.async_callback(self.finish))
        self.redirect('/lunch/%s' % lunch.id)
