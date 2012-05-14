from lib.database import db

class User(object):

    id = None
    name = None
    avatar_url = None

    def __init__(self, id, name, avatar_url, access_key, access_secret,
                 handle):
        self.id = id
        self.handle = handle
        self.name = name
        self.avatar_url = avatar_url
        self.access_key = access_key
        self.access_secret = access_secret

    @classmethod
    def create(cls, id, name, avatar_url, access_key, access_secret, handle):
        query = ('INSERT INTO users (id, name, avatar_url, access_key, '
                 'access_secret, handle) VALUES (%s, %s, %s, %s, %s, %s)')
        params = (id, name, avatar_url, access_key, access_secret, handle)
        db.execute(query, *params)
        return cls(id, name, avatar_url, access_key, access_secret, handle)

    @classmethod
    def get(cls, id):
        row = db.get('SELECT id, name, avatar_url, access_key, access_secret, '
                     'handle FROM users WHERE id = %s', int(id))
        if not row:
            return None

        return cls(**row)



