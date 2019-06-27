import hashlib
import random

class UserManager:

    def __init__(self, db, mediator):
        self.db = db
        self.mediator = mediator

    def login(self, options):
        user = self.db.getUser(options)
        if user:
            text = user['login'] + str(random.randint(0, 50000))
            token = hashlib.md5(text.encode('utf-8')).hexdigest()
            self.db.updateUserToken((token, user['id']))
            return { 'token': token, 'name': user['name']}
        return False

    def logout(self, options):
        user = self.db.getUserByToken(options)
        if user:
            self.db.updateUserToken(('', user['id']))
            return True
        return False

    def checkToken(self, token):
        user = self.db.getUserByToken(token)
        if user:
            return user['id']
        return False

    