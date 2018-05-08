from passlib.hash import pbkdf2_sha256
from pony.orm import db_session
from models import GP, App, Institution, Address


def hash_pass(password):
    return pbkdf2_sha256.hash(password)


@db_session
def check_login(username,password):

    user=GP.select(lambda u:u.username==username).first()
    if user:
        return pbkdf2_sha256.verify(password,user.password)
    return False


@db_session
def check_app_login(secret_key,name):

    app=App.select(lambda a:a.name==name)
    app=list(app)[0]
    return pbkdf2_sha256.verify(secret_key,app.secret_key)

