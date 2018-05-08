import datetime
from logging import log

import jwt
import re
from bottle import template, request, redirect, static_file, error, FormsDict, MultiDict, response
from pony.orm import db_session, ObjectNotFound

from decorators import require_uid, require_admin
from index import templates, ENTITY_DICT
from login import check_login, hash_pass
from models import Patient, Allergy, Medicalhistory, Institution, MedicalConditions, GP, Drug, \
    DrugHistory, SocialHistory, FamilyMedicalHistory, RadiologyAssesmentType, RadiologyAssesmentHistory, Symptom, \
    Address, db
from config import SECRET_KEY, app, TOKEN_TIME
from util import decode, jsonify_query, token_sent, search_value_table, fetch_item, fetch_all_items, create_item, \
    delete_item, get_relations, update_item, fetch_template, to_json


@app.route('/static/<filepath:path>', name='static')
def server_static(filepath):
    return static_file(filepath, root='./static/')


@app.route('/views/<filepath:path>', name='views')
def server_static(filepath):

    return static_file(filepath, root='./views/')

@app.route("/search")
@db_session
@require_uid
def search():
    if request.query:
        value=request.query["value"]
        criteria=None
        if "criteria" in request.query:
            criteria=request.query["criteria"]
        results = search_value_table(value,criteria)
        return results



@app.route("/user", method=["POST","GET", "DELETE", "PUT"])
@db_session
def home():
    data={}
    data["username"]=""
    data["STP"]=1
    data["TBP"]=1
    data["HP"]=2
    data["DP"]=6

    user_data=request.get_cookie("user_data",secret=SECRET_KEY)
    print(user_data)
    if user_data["admin"]:
        return template("admin.tpl")


    return template("index.html",data=data)



@app.route("/forms/<action>/<entity>")
@app.route("/forms/<action>/<entity>/<key>")
def open_forms(entity,action,key=None):


    if key:
        entity=ENTITY_DICT[entity][key]
        data=to_json(entity.to_dict(related_objects=True))
        print(data)
    tmpl=templates[action+"_"+entity]
    if "focus_patient" in app.config:
        patient_id=app.config["focus_patient"]

        return template(tmpl, data=data,username=app.config['username'],patient_id=patient_id)
    return template(tmpl, username=app.config['username'])

@app.route("/patient/<pid>/<entity>")
@db_session
def patient_data(entity,pid):
    data = getattr(Patient[pid], entity)
    route_template=templates["patient_"+entity]
    entity=ENTITY_DICT[entity]

    data=jsonify_query(data)
    print(data)
    return template(route_template,items=data)

@app.route("/admin/<entity>/<pid>", method=["PUT", "GET", "DELETE", "POST"])
@app.route("/admin/<entity>", method=["PUT", "GET", "DELETE", "POST"])
@db_session
def entity_all(entity=None,pid=None):

    if request.method == "GET":
        key=entity
        route_template = fetch_template("admin_"+entity, pid)
        entity = ENTITY_DICT[entity]

        if pid:

            data = fetch_item(entity,pid)
            if key=="patients":
                app.config["focus_patient"]=data["id"]
            return template(route_template,item=data)

        items=fetch_all_items(entity)
        print(items)
        return template(route_template,items=items)

    elif request.method == "POST":
        json = request.POST

        if entity=="medreport":
            json["patient"]=app.config["focus_patient"]
            json["date"]=datetime.datetime.now().date()
            json["time"]=datetime.datetime.now().time()
            json["origin"]=app.config["user_id"]

        entity=ENTITY_DICT[entity]
        return create_item(entity,json)


    elif request.method == "DELETE":
        if pid:
            return delete_item(entity,pid)
        return {"message":"missing id"}

    elif request.method == "PUT":
            update_item(Patient,pid,request.query)
            return {"message": "patient updated"}
    return {"message": "missing token"}


@app.route("/user/<entity>/<pid>", method=["PUT", "GET", "DELETE", "POST"])
@app.route("/user/<entity>",method=["PUT", "GET", "DELETE", "POST"])
@db_session
def entity_all(entity,pid=None):

    if request.method == "GET":
        key=entity
        route_template = fetch_template(entity, pid)
        entity = ENTITY_DICT[entity]

        if pid:

            data = fetch_item(entity,pid)
            print(data)
            return template(route_template,item=data)

        items=fetch_all_items(entity)
        print(items)
        return template(route_template,data=items)

    elif request.method == "POST":
        json = request.POST

        print("here")
        for i,k in json.items():
            print(i,k)
        if entity=="medhistory":

            #json["patient"]=app.config["focus_patient"]
            json["date"]=datetime.datetime.now().date()
            json["time"]=datetime.datetime.now().time()
            #json["origin"]=app.config["user_id"]

        entity=ENTITY_DICT[entity]

        entity=create_item(entity,json)
        print("before-return")
        return entity


    elif request.method == "DELETE":
        if pid:
            return delete_item(entity,pid)
        return {"message":"missing id"}

    elif request.method == "PUT":
            for i in request.headers.items():
                print(i)
            print(request.json)
            update_item(Patient,pid,request.query)
            return {"message": "patient updated"}
    return {"message": "missing token"}


@app.route("/data/<entity>/<pid>", method=["PUT", "GET", "DELETE", "POST"])
@app.route("/data/<entity>",method=["PUT", "GET", "DELETE", "POST"])
@db_session
def entity_all(entity,pid=None):

    if request.method == "GET":
        key=entity
        entity = ENTITY_DICT[entity]

        if pid:

            data = fetch_item(entity,pid)
            return data

        items=fetch_all_items(entity)
        print(items)
        return items

    elif request.method == "POST":
        json = request.POST
        print("here")
        for i,k in json.items():
            print(i,k)
        if entity=="medreport":
            json["patient"]=app.config["focus_patient"]
            json["date"]=datetime.datetime.now().date()
            json["time"]=datetime.datetime.now().time()
            json["origin"]=app.config["user_id"]

        entity=ENTITY_DICT[entity]
        print("entity")
        entity=create_item(entity,json)
        print("before-return")
        return entity


    elif request.method == "DELETE":
        if pid:
            return delete_item(entity,pid)
        return {"message":"missing id"}

    elif request.method == "PUT":
        if pid:
            json=request.query
            entity_cls=ENTITY_DICT[entity]
            update_item(entity_cls,pid,json)
            return {"message": "patient updated"}

@app.route("/")
@app.route("/login", method=["GET", "POST"])
@db_session
def login():
    """manage login page"""

    if request.method == "POST":
        username = request.POST.username.strip()
        password = request.POST.password.strip()
        # check for valid user credentials
        # set token
        if check_login(username, password):
            user = GP.select(lambda user: user.username == username).first()
            print("in")
            # set required user information
            # response.set_cookie("username",user.username)
            # response.set_cookie("user_id",user.id)
            # response.set_cookie("admin",user.admin)

            app.config["username"] = user.username
            app.config["user_id"] = user.id
            app.config["admin"]=user.admin

            # set logged in token
            token = jwt.encode({"exp": TOKEN_TIME}, SECRET_KEY, algorithm="HS256")
            app.config["logged_in_token"] = token

            response.headers["x-access-token"]=token
            response.set_cookie("x-access-token",token,httponly=True,expires=TOKEN_TIME,secret=SECRET_KEY)
            response.set_cookie("user_data",{"userid":user.id,"username":user.username,"admin":user.admin},expires=TOKEN_TIME,secret=SECRET_KEY)


            # default redirect
            redirect("/user")

        return template("login.html", message="Invalid username or password")

    return template("login.html", message="")

@app.error(500)
def error500(error):
    return "SOMETHING WRONG WITH THE SERVER"


@app.error(404)
def error404(error):
    return "Page not found"


@app.route("/logout")
@require_uid
def logout():
    app.config["logged_in_token"] = None
    app.config["username"] = None
    app.config["user_id"] = None
    redirect("/login", 404)

if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)

