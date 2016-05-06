from google.appengine.ext import ndb
import pbkdf2
import uuid

TEST_MODE = False # True

def hash_pwd(pwd_text):
    salt = "AF6FD01D57DD3DD71EAAAE2C225B1AD740FAADD575B6D68D6A3507D4DC8D9AD8"
    return pbkdf2.pbkdf2_hex(pwd_text.encode('utf-8'), salt)    

def is_admin(token):
    if TEST_MODE and token == "!admin": return True
    u = user_for_token(token)
    return u is not None and u.is_admin

def is_valid(token):
    if TEST_MODE and token in ('!admin', '!user'): return True
    u = user_for_token(token)
    return u is not None

def user_for_token(token):
    if token == '': return None
    tk = ndb.Key(LoginToken, token).get()
    if tk:
        return ndb.Key(User, tk.email).get()
    else:
        return None

def create_default_admin_user_if_nonexistent():
    email = 'admin@admin.com'
    pwd = 'jellywatch383703'
    a = User.with_email(email)
    if not a:
        User.create_user(email, pwd, False, True)

class User(ndb.Model):
    @classmethod
    def with_email(cls, email):
        return ndb.Key(User, email).get()
    
    @classmethod
    def create_user(cls, email, pwd, is_organization, is_admin):
        # returns (new user or None, error)
        user = User.get_or_insert(email)
        if user.pwd_hash != None:
            # this user already exists
            return False, "A user with that email already exists."
        user.pwd_hash = hash_pwd(pwd)
        user.is_organization = is_organization
        user.is_admin = is_admin
        user.put()
        return user, None
    
    @classmethod
    def create_login_token(cls, email, pwd):
        # returns a login token string or null
        create_default_admin_user_if_nonexistent()
        user = ndb.Key(User, email).get()
        if user and user.pwd_hash == hash_pwd(pwd):
            token = uuid.uuid4().hex
            token = LoginToken(id=token, email=email)
            token.put()
            return token.key.id()
        else:
            return None
    
    pwd_hash = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    is_organization = ndb.BooleanProperty()
    is_admin = ndb.BooleanProperty()
    
    def to_json(self):
        return {"email": self.key.id(), "is_admin": self.is_admin, "is_organization": self.is_organization}

class LoginToken(ndb.Model):
    email = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
