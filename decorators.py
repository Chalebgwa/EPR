from bottle import request, redirect, template
from pony.orm import db_session

from models import User, GP
from config import app
import jwt
from config import SECRET_KEY

@db_session
def require_uid(fn):
    """decorator to check if user has been authourized"""
    def check_uid(*args, **kwargs):
        #check if logged in token exists
        try:
            #fetch token if user already logged in
            if "x-access-token" in request.cookies:

                token=request.get_cookie("x-access-token",secret=SECRET_KEY)
                try:
                    jwt.decode(token,SECRET_KEY,algorithms="HS256")
                    return fn(*args, **kwargs)
                except:
                    return {"message":'invalid token'}

            return {"message":"missing token"}
        except KeyError:
            #fetch redirect
            next=request.fullpath
            redirect("/login")
    return check_uid



@db_session
def require_admin(fn):
    """for routes that require admin access"""
    def check_admin(*args,**kwargs):

        id=app.config["user_id"]
        if GP[id].admin:
            return fn(*args,**kwargs)

        return redirect("/user")


    return check_admin
