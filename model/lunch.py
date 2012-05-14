from lib.database import db

from model.user import User

class Lunch(object):

    id = None
    food = None
    place = None
    lunch_date = None
    slots = None
    creator_id = None

    def __init__(self, id, food, place, lunch_date, creator_id, slots,
                 tags=[]):
        self.id = id
        self.food = food
        self.place = place
        self.lunch_date = lunch_date
        self.creator_id = creator_id
        self.slots = slots
        self.tags = tags

    @classmethod
    def create(cls, food, place, lunch_date, creator_id, slots, tags=[]):
        query = ('INSERT INTO lunch '
                '(food, place, lunch_date, creator_id, slots) '
                'VALUES (%s, %s, %s, %s, %s)')
        params = (food, place, lunch_date, creator_id, slots)
        db.execute('BEGIN')
        id = db.execute(query, *params)

        new_tags = []
        try:
            for tag in tags:
                new_tags.append(LunchTag.create(id, tag))
        except:
            db.execute('ROLLBACK')
            return None
        db.execute('COMMIT')
        return cls(id, food, place, lunch_date, creator_id, tags)

    @classmethod
    def get(cls, id):
        row = db.get('SELECT id, food, place, lunch_date, creator_id, slots '
                     'FROM lunch WHERE id = %s', int(id))
        if not row:
            return None

        import logging
        logging.error(row)
        instance = cls(**row)
        #['id'], row['food'], row['place'], row['lunch_date'],
        #row['creator_id'])

        tags = LunchTag.get_all(instance.id)
        instance.tags = tags
        return instance


    @classmethod
    def get_page(cls, page=0):
        PER_PAGE = 20

        offset = int(page) * PER_PAGE
        limit = offset + PER_PAGE
        rows = db.query('SELECT id, food, place, lunch_date, creator_id, '
                        'slots '
                        'FROM lunch ORDER BY lunch_date DESC LIMIT %s,%s', offset, limit)
        if not rows:
            return None

        instances = []
        for row in rows:
            instance = cls(**row)
            instance.tags = LunchTag.get_all(instance.id)
            instances.append(instance)
        return instances

    def get_participants(self):
        rows = db.query('SELECT user_id FROM lunch_participants '
                     'WHERE lunch_id=%s', int(self.id))
        if not rows:
            return None

        participants = []
        for row in rows:
            participants.append(User.get(row['user_id']))

        return participants

    participants = property(get_participants)

    def add_participant(self, user_id):
        if self.slots <= 0:
            raise ValueError("no slots left")

        db.execute('BEGIN')
        query = ('INSERT INTO lunch_participants (lunch_id, user_id) '
                'VALUES (%s, %s)')
        params = (int(self.id), int(user_id))
        id = db.execute(query, *params)
        try:
            db.execute('UPDATE lunch SET slots=slots-1 WHERE id = %s',
                       int(self.id))
        except:
            db.execute('ROLLBACK')
            return None

        db.execute('COMMIT')
        return id


class LunchTag(object):

    lunch_id = None
    tag = None

    def __init__(self, id, lunch_id, tag):
        self.id = id
        self.lunch_id = lunch_id
        self.tag = tag


    @classmethod
    def create(cls, lunch_id, tag):
        query = 'INSERT INTO lunch_tags (lunch_id, tag) VALUES (%s, %s)'
        params = (lunch_id, tag)
        id = db.execute(query, *params)
        return cls(id, lunch_id, tag)

    @classmethod
    def get_all(cls, lunch_id):
        rows = db.query('SELECT id, lunch_id, tag FROM lunch_tags '
                        'WHERE lunch_id = %s',
                        int(lunch_id))
        if not rows:
            return None

        tags = []
        for row in rows:
            tags.append(cls(**row))

        return tags

    def __repr__(self):
        return str(self.tag)
