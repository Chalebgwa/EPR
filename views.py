import datetime
from logging import log

import jwt
from bottle import template, request, redirect, static_file, error
from pony.orm import db_session, ObjectNotFound

from decorators import require_uid
from login import check_login, hash_pass
from models import Patient, Allergy, Medicalhistory, Institution, MedicalConditions, GP, Drug, \
    DrugHistory, SocialHistory, FamilyMedicalHistory, RadiologyAssesmentType, RadiologyAssesmentHistory, Symptom, \
    Address, db
from config import SECRET_KEY, app, TOKEN_TIME
from util import decode, jsonify_query, token_sent, search_value_table, index


@app.route('/static/<filepath:path>', name='static')
def server_static(filepath):
    return static_file(filepath, root='./static/')


@app.route("/patients/create")
def create_patient():
    return template("pcreate.html")


# todo : secure path
@app.route("/patient/<itemid>")
@db_session
def patient_all(itemid):
    patient = Patient[itemid]
    return template("patientProfile.html", item=patient)


@app.route("/patients", method=["PUT", "GET", "DELETE", "POST"])
@db_session
@require_uid
def patient_all():
    if request.method == "GET":
        records = Patient.select()
        return template("index.html", items=records)

    elif request.method == "POST":
        json = request.POST

        # check to see if request has provided all necessary values to create object
        #

        name = json["pname"]
        surname = json["surname"]
        dob = json["dob"]
        gp = GP[app.config["user_id"]]
        status = True
        city = json["city"]
        district = json["district"]

        address = Address(cityName=city, districtName=district, districtCode="fix this")

        patient = Patient(name=name,
                          sex="fix this",
                          dob=dob,
                          address=address,
                          gp=gp,
                          status=status)
        #save progress
        db.commit()

        #redirect to the newly created patient's page
        redirect("/patient/{}".format(patient.id))

    elif request.method == "DELETE":

        patient_id = request.POST.id.strip()
        try:
            patient = Patient[patient_id]
        except:
            return "Patient does not exist"
        patient.delete()

    elif request.method == "PUT":
        json = request.POST
        update = json["update"]
        value = json["value"]
        id = json["id"]
        with db_session():
            try:
                patient = Patient[id]
            except:
                return {"message": 'patient not found'}
            setattr(patient,update,value)
            return {"message": "patient updated"}
    return {"message": "missing token"}


@app.route("/login", method=["GET", "POST"])
@db_session
def login():
    """manage login page"""

    # if route accessed by redirect from decorated route
    if request.query:
        rdr = request.query["rdr"]
        app.config["rdr"] = "/{}".format(rdr)

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
            if "rdr" in app.config.keys():
                rdr = app.config.pop("rdr")
                redirect(rdr)

            # default redirect
            redirect("/patients")

    return template("views/login.html")


# @app.route("/app_login",method=["GET","POST"])
# @db_session
# def app_login():
#     json=token_sent(request)
#     cipher = Fernet(SECRET_KEY)
#     if request.method=="POST" and json:
#         app_name=json["name"]
#         secret_key=json["secret_key"]
#         cipher.decrypt(secret_key)
#         key=cipher.decrypt(secret_key)
#
#
@app.route("/register", method=["GET", "POST"])
@db_session
def register_user():
    json = request.POST
    if request.method == "POST" and json:
        try:
            address = json["address"]
            name = json["name"]
            password = hash_pass(json["password"])
            username = json["username"]
            institution_id = json["hospital"]
            admin = json["admin"]
            institution = Institution[institution_id]
        except:
            return {"message": "missing user values"}

        GP(address=address, name=name, username=username, hospital=institution, admin=admin, password=password)
        return {"message": "user created!!"}
    if request.method == "GET":
        return template("templates/regiter.html")



@app.route("/user", method=["PUT", "GET", "DELETE", "POST"])
@db_session
@require_uid
def user():
    if request.method == "GET":
        json=request.GET
        if not json:
            users = GP.select()
            return jsonify_query(users)

        try:
            user_id = json["user_id"]
            user = GP[user_id]
            return user.to_dict()
        except:
            return {"message": "missing user_id"}

    if request.method == "PUT":

        json=request.POST
        try:
            name = json["name"]
            address = json["address"]
            username = json["username"]
            password = json["password"]
            work = json[""]
        except KeyError:
            return {"message": "missing data values"}
        user = GP(password=password, name=name, username=username, address=address)
        return {"message": "user created"}

    if request.method == "POST":
        json=request.POST
        try:
            user_id = json["user_id"]
            update = json["update"]
            value = json["value"]
        except KeyError:
            return {"message": "missing data values"}

        user = GP[user_id]
        setattr(user,update,value)
        return {"message": "user updated"}
    if request.method == "DELETE":
        json=request.POST
        try:
            user_id = json["user_id"]
        except KeyError:
            return {"message": "please provide valid user_id"}

        user = GP[user_id]
        user.delete()
        return {"message": "user deleted"}
    return {"message": "missing token"}


@app.route("/patients/medicalReport", method=["PUT", "GET", "DELETE", "POST"])
@db_session
# @require_uid
def medReport():
    if request.method=="GET":
        return template("CreateCReport.html")


@app.route("/patients/medicalReport", method=["PUT", "GET", "DELETE", "POST"])
@db_session
# @require_uid
def patient():
    return template("CreateCReport.html")


@app.route("/patients/profile", method=["PUT", "GET", "DELETE", "POST"])
@db_session
# @require_uid
def patient():
    return template("patientProfile.html")


# @app.route("/allergy",method=["PUT","GET","DELETE","POST"])
# @db_session
# @require_uid
# def allergy():
#
#     json=token_sent(request)
#
#     if request.method=="PUT" and json:
#         try:
#             allergy=Allergy(allergy_name=json["allergy_name"])
#             symptoms=json["symptoms"]
#
#         except:
#             return {"message":"name value missing"}
#
#         sms=[]
#         for symptom in symptoms:
#             sms.append(Symptom[symptom])
#
#         allergy.symptoms=sms
#
#         return {"message":"new allergy added"}
#
#     elif request.method=="GET":
#
#         if json:
#             try:
#                 id=json["id"]
#                 allergy=Allergy[id]
#                 symptoms=allergy.symptoms
#
#                 return {
#                     "allergy":allergy.to_dict(),
#                     "symptoms":[s.name for s in symptoms]
#                 }
#             except:
#                 return {"message":"Please provide id"}
#
#         records=Allergy.select()
#         return jsonify_query(records)
#
#     elif request.method=="POST" and json:
#
#         try:
#             id=json["id"]
#             name=json["allergy_name"]
#             allergy = Allergy[id]
#             allergy.name = name
#             return {"message": "updated"}
#         except:
#             return {"message":"Please provide id"}
#
#     elif request.method=="DELETE" and json:
#         try:
#             id = json["id"]
#             allergy=Allergy[id]
#             allergy.delete()
#
#             return {"message":"deleted"}
#         except:
#             return {"message":"please provide valid id"}
#     return {'message':"missing token"}
#

@app.route("/user/patients/medreport", method=["GET"])
@db_session
def medreport():
    if request.method == "GET":
        return template("medicalHList.html")


@app.route("/user/patients/medreport/new", method=["GET", "POST"])
@db_session
def addMedReport():
    if request.method == "POST":
        return request.POST

    return template("createCReport.html")


@app.error(500)
def error500(error):
    return "Error 500"


@app.error(404)
def error404(error):
    return "Page not found"


# @app.route("/institution",method=["POST","GET"])
# @db_session
# def institution():
#     json=token_sent(request)
#
#     if request.method=="GET":
#         if json:
#             try:
#                 institution=Institution[json["id"]]
#                 return institution.to_dict()
#             except:
#                 return {"message":"missking key"}
#
#         records=Institution.select()
#         return jsonify_query(records)
#     if request.method=="POST" and json:
#
#         try:
#             name=json["name"]
#             insttype=json["insttype"]
#         except:
#             return {"message":"missing keys"}
#
#         Institution(name=name,insttype=insttype)
#
#         return {"message":"Hospital created"}
#
#     return {"message":"missing token"}
#
#
#
# @app.route("/visit",method=["PUT","GET","DELETE","POST"])
# @db_session
# @require_uid
# def visitHistory():
#
#     json=token_sent(request)
#
#
#     if request.method=="GET":
#         if json:
#             try:
#                 patient_id=json["patient_id"]
#                 patient=Patient[patient_id]
#                 records=VisitHistory.select(lambda v:v.patient==patient)
#             except:
#                 return {"message":"missing patient id"}
#         else:
#             records=VisitHistory.select()
#
#         return jsonify_query(records)
#
#     elif request.method=="POST" and json:
#
#         if json["update"] and json["value"] and json["patient_id"]:
#             id=json["patient_id"]
#             update=json['update']
#             value=json["value"]
#             patient=Patient[id]
#
#             visits=VisitHistory.select(lambda p:p.patient==patient)
#
#             for visit in visits:
#                 if update=='date':
#                     visit.date=value
#                 if update=="time":
#                     visit.time=value
#                 if update=="patient":
#                     visit.patient=Patient[value]
#                 if update=="episode_number":
#                     visit.episode_number=value
#                 if update=="diagnosis":
#                     visit.diagnosis=MedicalConditions[value]
#                 if update=="hospital":
#                     visit.hospital=Institution[value]
#                 if update=="gp":
#                     visit.intervention=GP[value]
#
#                 return {"message":"records updated"}
#
#     elif request.method=="DELETE":
#         date=json["date"]
#         time=json["time"]
#         patient=Patient[json["patient_id"]]
#         records=VisitHistory.select(lambda v:v.date==date and
#                                              v.patient==patient and
#                                              v.time==time)
#         for record in records:
#             record.delete()
#         return {"message":"deleted"}
#
#     elif request.method=="PUT":
#
#         if request.query:
#
#             try:
#                 patient = json["patient"]
#                 episode_number = json["episode_number"]
#                 diagnosis = MedicalConditions[json["diagonosis"]]
#                 hospital = json["hospital"]
#                 gp = json["gp"]
#             except:
#                 return {"missing":"data values"}
#
#             visit=VisitHistory(patient=patient,episode_number=episode_number,diagnosis=diagnosis,hospital=hospital,gp=gp)
#
#             return {"message":"new record saved"}
#
# @app.route("/drug_history",method=["PUT","GET","DELETE","POST"])
# @db_session
# @require_uid
# def drug_history():
#
#
#     if request.method=="PUT":
#         data=request.query["token"]
#         json=decode(data)
#         history=DrugHistory(status=json["status"],start=json["start"],end=json["start"],
#                             drug=Drug[json["drug"]],dose=json["dose"],
#                             frequency=json["frequency"],repeat_prescription=json["repeat_prescription"],
#                             patient=Patient[json["patient"]],gp=GP[json["gp"]])
#         return {"message":"new history updated"}
#
#     elif request.method=="GET":
#         data=request.query['token']
#         json=decode(data)
#         patient=Patient[json["patient_id"]]
#         records=DrugHistory.select(lambda d:d.patient==patient)
#
#         return jsonify_query(records)
#
# @app.route("/socialhistory",method=["PUT","GET","DELETE","POST"])
# @db_session
# @require_uid
# def social_history():
#     data = request.query["token"]
#     json = decode(data)
#
#     if request.method=="PUT":
#
#         patient=Patient[json["patient"]]
#         description=json["description"]
#         frequency=json["frequency"]
#         onset=json["onset"]
#         condition=MedicalConditions[json["condition"]]
#
#         socialhistory=SocialHistory(condition=condition,patient=patient,description=description,frequency=frequency,onset=onset)
#
#         return {"message":"ok"}
#     if request.method=="GET":
#
#         patient_id=json["patient"]
#         patient=Patient[patient_id]
#         records=SocialHistory.select(lambda r:r.patient==patient)
#         return jsonify_query(records)
#     elif request.method=="POST":
#
#         id=request.query["id"]
#         update=request.query["update"]
#         value=request.query["value"]
#
#         record=SocialHistory[id]
#
#         if update=="condition":
#             record.condition=value
#         if update=="description":
#             record.description=value
#         if update=="frequency":
#             record.frequecy=value
#         if update=="onset":
#             record.onset=value
#
#         return {"message":"OK"}
#
#     elif request.method=="DELETE":
#         id=json["id"]
#         record=SocialHistory[id]
#         record.delete()
#         return {"message":"deleted"}
#
# @app.route("/familyhistory",method=["PUT","GET","DELETE","POST"])
# @db_session
# @require_uid
# def fam_history():
#
#     if request.query:
#         data = request.query["token"]
#         json = decode(data)
#     else:
#         return {"message":"missing data values"}
#
#     if request.method == "PUT":
#         try:
#             patient = Patient[json["patient"]]
#             relation = Patient[json["relation"]]
#             relationship=json["relationship"]
#             comments = json["comments"]
#             onset = json["onset"]
#             condition = MedicalConditions[json["condition"]]
#
#         except KeyError:
#             return {"message":"missing data values"}
#
#         history = FamilyMedicalHistory(condition=condition, patient=patient, commenents=comments,
#                                       relation=relation, relationship=relationship,onset_age=onset)
#
#         return {"message": "ok"}
#
#     if request.method == "GET":
#
#         patient_id = json["id"]
#         patient=Patient[patient_id]
#         records = FamilyMedicalHistory.select(lambda r: r.patient == patient)
#         return jsonify_query(records)
#
#     elif request.method == "POST":
#
#         id = request.query["id"]
#         update = request.query["update"]
#         value = request.query["value"]
#
#         record = SocialHistory[id]
#
#         if update == "condition":
#             record.condition = value
#         if update == "description":
#             record.description = value
#         if update == "frequency":
#             record.frequecy = value
#         if update == "onset":
#             record.onset = value
#
#         return {"message": "OK"}
#
#     elif request.method == "DELETE":
#         id = json["id"]
#         record = FamilyMedicalHistory[id]
#         record.delete()
#         return {"message": "deleted"}
#
# @app.route("/radiologyhistory",method=["PUT","GET","DELETE","POST"])
# @db_session
# @require_uid
# def radiology():
#
#     if request.query:
#         data=request.query["token"]
#         json=decode(data)
#     else:
#         return {"message":"token missing"}
#
#     if request.method=="PUT":
#         try:
#             date=json["date"]
#             test_type=RadiologyAssesmentType[json["test_type"]]
#             result=MedicalConditions[json["result"]]
#             requesting_physcian=GP[json["requesting_physcian"]]
#         except KeyError:
#             return {"message":"missing data values"}
#
#         radiologyAssessment=RadiologyAssesmentHistory(date=date,test_type=test_type,result=result,requesting_physcian=requesting_physcian)
#         return {"message":"history updated"}
#
#     if request.method=="GET":
#         try:
#             patient_id=json["patient_id"]
#             patient=Patient[patient_id]
#         except KeyError:
#             return {"message":"missing data values"}
#
#         records=RadiologyAssesmentHistory.select(lambda rah:rah.patient==patient)
#         return jsonify_query(records)
#
#     if request.method=="POST":
#         try:
#             update=json["update"]
#             id=json["id"]
#             value=json["value"]
#         except KeyError:
#             return {"message":"data values missing"}
#
#         rah=RadiologyAssesmentHistory[id]
#
#
#
#
#         if update=="test_type":
#             rah.test_type=RadiologyAssesmentType[value]
#         if update=="result":
#             rah.result=MedicalConditions[value]
#         if update=="requesting_physcian":
#             rah.requesting_physcian=value
#         if update=="date":
#             rah.date=value
#
#         else:
#             return {"message":"update value does not match existing fields"}
#         return {"message":"updated"}
#     if request.method=="DELETE":
#         try:
#             id=json["id"]
#         except:
#             return {"message":"missing id value"}
#
#         rah=RadiologyAssesmentHistory[id]
#         rah.delete()
#         return {"message":"record deleted"}
#
#
# @app.route("/radiologytype",method=["PUT","GET","DELETE","POST"])
# @db_session
# @require_uid
# def radiology_test_type():
#     if request.query:
#         data=request.query["token"]
#         json=decode(data)
#     else:
#         return {"message":"token is missing"}
#
#     if request.method=="GET":
#         if json["id"]:
#             id=json["id"]
#         else:
#             return {"message":"missing id value"}
#         return RadiologyAssesmentType[id].to_dict()
#     if request.method=="PUT":
#         if json["name"]:
#             name=json["name"]
#         else:
#             return {"message":"missing name value"}
#
#         rat=RadiologyAssesmentType(name=name)
#         return {"message":"updated"}
#     if request.method=="POST":
#         if json["id"]:
#             id=json["id"]
#             update=json["update"]
#             value=json["value"]
#         else:
#             return {"message":"missing id value"}
#         rat = RadiologyAssesmentType[id]
#         if update=="name":
#             rat.name=value
#             return {"message":"updated"}
#         return {"message":"update value doesnt match existing field"}
#
#     if request.method=="DELETE":
#         if json["id"]:
#             id=json["id"]
#         else:
#             return {"message":"missing id value"}
#         rat = RadiologyAssesmentType[id]
#         rat.delete()
#         return {"message":"record deleted"}
#
#
# @app.route("/drug",method=["PUT","GET","DELETE","POST"])
# @db_session
# @require_uid
# def drug():
#     if request.query:
#         data = request.query["token"]
#         json = decode(data)
#     else:
#         return {"message": "token is missing"}
#
#     if request.method == "GET":
#         if json["id"]:
#             id = json["id"]
#         else:
#             return {"message": "missing id value"}
#
#         return Drug[id].to_dict()
#     if request.method == "PUT":
#         if json["name"]:
#             name = json["name"]
#         else:
#             return {"message": "missing name value"}
#
#         drug = Drug(name=name)
#         return {"message": "updated"}
#     if request.method == "POST":
#         if json["id"]:
#             id = json["id"]
#             update = json["update"]
#             value = json["value"]
#         else:
#             return {"message": "missing id value"}
#         drug = Drug[id]
#         if update == "name":
#             drug.name = value
#             return {"message": "updated"}
#         return {"message": "update value doesnt match existing field"}
#
#     if request.method == "DELETE":
#         if json["id"]:
#             id = json["id"]
#         else:
#             return {"message": "missing id value"}
#         drug = Drug[id]
#         drug.delete()
#         return {"message": "record deleted"}
#
@app.route("/logout")
@require_uid
def logout():
    app.config["logged_in_token"] = None
    app.config["username"] = None
    app.config["user_id"] = None
    redirect("/login", 404)


#
#
#
# @app.route("/districts")
# def districts():
#     json=token_sent(request)
#
#     if request.method=="GET":
#         if json:
#             try:
#                 id=json["id"]
#             except:
#                 return {"message":"define id for entity"}
#         else:
#             records=District.select()
#             return jsonify_query(records)
#
#
#
if __name__ == "__main__":
    app.run(host="localhost", port=8080, debug=True)
