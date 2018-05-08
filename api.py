import asyncio

import pickle
from bottle import static_file, response
from pip._vendor.cachecontrol import serialize
from pip._vendor.cachecontrol.serialize import Serializer
from pony.orm.serialization import to_json

from config import *
from decorators import *
from index import *
from login import *
from util import *

from gevent.pywsgi import WSGIServer

@app.route("/search")
@db_session
def search():
    if request.query:
        query = request.query["q"]
        results = search_value_table(query, "allergie")

        response.body={"message":"testing"}
        return jsonify_query(results,True)





@app.route("/user/<entity>/<pid>", method=["PUT", "GET", "DELETE", "POST"])
@app.route("/user/<entity>", method=["PUT", "GET","POST"])
@db_session
@require_uid
def entity_all(entity,pid=None):

    entity=ENTITY_DICT[entity]

    if request.method == "GET":
        if pid:
            data=fetch_item(entity,pid)

        else:
            return fetch_all_items(entity)

    elif request.method == "POST":
        json = request.POST
        return create_item(entity,json)

    elif request.method == "DELETE":
        if pid:
            return delete_item(entity,pid)
        return {"message":"missing id"}

    elif request.method == "PUT":
            update_item(Patient,pid,request.query)
            return {"message": "patient updated"}
    return {"message": "missing token"}


@app.route("/login", method=["GET", "POST"])
@db_session
def login():
    """manage login page"""

    # if route accessed by redirect from decorated route
    if request.query:
        rdr = request.query["redirect"]
        rdr="/"+rdr




    if request.method == "POST":
        username = request.POST.username.strip()
        password = request.POST.password.strip()

        # check for valid user credentials
        # set token
        if check_login(username, password):
            user = GP.select(lambda user: user.username == username).first()

            # set required user information
            app.config["username"] = user.username
            app.config["user_id"] = user.id

            # set logged in token
            token = jwt.encode({"exp": TOKEN_TIME}, SECRET_KEY, algorithm="HS256")
            app.config["logged_in_token"] = token

            # redirect to route given by decorator
            if rdr:

                redirect(rdr)

            # default redirect
            return {"message":"access granted",'token':str(token)}

    return {"message":"provide valid credentials"}

@app.route("/logout")
@require_uid
def logout():
    app.config["logged_in_token"] = None
    app.config["username"] = None
    app.config["user_id"] = None
    redirect("/login")

if __name__ == "__main__":
    http = WSGIServer(('localhost', 8080), app)
    http.serve_forever()

