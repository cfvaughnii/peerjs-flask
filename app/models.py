from app import users

class User():
    id = 0
    nickname = users[id]["nickname"]

    def __init__(self, id=-1, nickname=None):
        print "User init ",id, 
        if nickname is not None:
            print nickname
        print
        self.id = 0
        self.nickname = users[self.id]["nickname"]
        if int(id) >= 0:
            print "id >= 0 ",id, 
            self.id = int(id)
            self.nickname = users[self.id]["nickname"]
        
        if nickname is not None:
            self.set_user(nickname) 

    def set_user(self, nickname):
        print "set_user",nickname, 
        id=0
        for u in users:
            if u["nickname"] == nickname:
                print "found",nickname, 
                self.id = id
                self.nickname = users[id]["nickname"]
                break
            id += 1
        print "set_user", self.nickname

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            print "get_id",self.id
            return unicode(self.id)  # python 2
        except NameError:
            return str(self.id)  # python 3

    def __repr__(self):
        return '<User %r>' % (self.nickname)
