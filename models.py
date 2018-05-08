from pony import orm
from datetime import date,time


db=orm.Database()
db.bind(provider='mysql', host='localhost', user='root', passwd='', db='epr')

class History(db.Entity):
    entity_class=orm.Required(str)
    data=orm.Required(bytes)
    entity_id=orm.Required(int)
    date=orm.Required(date)

class User(db.Entity):
   name=orm.Required(str)
   surname=orm.Required(str)
   number=orm.Optional(int)
   email=orm.Optional(str)
   admin=orm.Required(bool)
   password=orm.Required(str)


   def promote(self):
       self.admin=True



class App(db.Entity):
    name=orm.Required(str)
    secret_key=orm.Required(str)




class Institution(db.Entity):
    name=orm.Required(str)
    insttype = orm.Required(str)
    Gps = orm.Set("GP")

    medhistories=orm.Set("Medicalhistory",reverse="institution")

class Allergy(db.Entity):

    allergy_name=orm.Required(str)
    patients=orm.Set("Patient")
    symptoms=orm.Set("Symptom",reverse="allergy")

class Medicalhistory(db.Entity):
    date = orm.Required(date)
    time = orm.Required(time)
    patients=orm.Required("Patient")
    diagnosis=orm.Required(str)
    origin=orm.Required("GP")
    episode_number = orm.Required(int)
    institution = orm.Required(Institution)
    intervention = orm.Required(str)


class GP(db.Entity):
    address=orm.Set(lambda: Address)
    name=orm.Required(str)
    patients=orm.Set("Patient")
    username=orm.Required(str)
    password=orm.Required(str)
    hospital=orm.Required(Institution)
    admin=orm.Required(bool)
    email=orm.Required(str)
    surname=orm.Required(str)
    number=orm.Required(str)
    assessments=orm.Set("RadiologyAssesment",reverse="radiologist")
    requests=orm.Set("RadiologyAssesment",reverse="requesting_physician")
    medhistories=orm.Set("Medicalhistory",reverse="origin")
    drugsAdministered=orm.Set("DrugHistory",reverse="gp")
    radiologyAssesmentHistory=orm.Set("RadiologyAssesmentHistory",reverse="requesting_physician")



class Patient(db.Entity):
    name=orm.Required(str)
    surname=orm.Required(str)
    dob=orm.Required(str)
    number=orm.Required(str)
    sex=orm.Required(str)
    allergy=orm.Set(Allergy,reverse="patients")
    address=orm.Required(lambda: Address)
    gp=orm.Required(GP,reverse="patients")
    status=orm.Required(bool)
    drug_history=orm.Set("DrugHistory",reverse="patients")
    medhistory=orm.Set("Medicalhistory",reverse="patients")
    familyhistory=orm.Set("FamilyMedicalHistory",reverse="patients")
    famhistory_relation=orm.Set("FamilyMedicalHistory",reverse="relation")
    socialhistory=orm.Set("SocialHistory",reverse="patients")
    radiology=orm.Set("RadiologyAssesment",reverse="patients")

class Address(db.Entity):
   gps = orm.Set(GP)
   patients = orm.Set(Patient)
   districtName=orm.Required(str)
   districtCode=orm.Required(str)
   cityName=orm.Required(str)
   vTown=orm.Optional(str)

class SocialHistory(db.Entity):
    condition=orm.Required("MedicalConditions")
    description=orm.Required(str)
    frequency=orm.Required(str)
    onset=orm.Required(date)
    patients=orm.Required(Patient)

class FamilyMedicalHistory(db.Entity):
    condition=orm.Required("MedicalConditions")
    patients=orm.Required(Patient)
    relation=orm.Required(Patient)
    relationship=orm.Required(str)
    onset_age=orm.Required(int)
    comments=orm.Required(str)


class RadiologyAssesmentHistory(db.Entity):
    date=orm.Required(date)
    test_type=orm.Required(str)
    result=orm.Required("MedicalConditions")
    requesting_physician = orm.Required(GP)

class District(db.Entity):
    name=orm.Required(str)

class Drug(db.Entity):
    drug_id=orm.PrimaryKey(int,auto=True)
    name=orm.Required(str)

    history=orm.Set("DrugHistory",reverse="drug")


class DrugHistory(db.Entity):
    status=orm.Required(bool)
    start=orm.Required(date)
    end=orm.Required(date)
    drug=orm.Required(Drug)
    dose=orm.Required(str)
    frequency=orm.Required(str)
    repeat_prescription=orm.Required(str)
    patients=orm.Required(Patient)
    gp=orm.Required(GP)

class Search_history(db.Entity):
    user_id=orm.Required(int)
    search=orm.Required(str)
    date=orm.Required(date)


class MedicalConditions(db.Entity):
    mc_id=orm.PrimaryKey(int,auto=True)
    name=orm.Required(str)
    radiologyAssesment=orm.Set("RadiologyAssesment",reverse="result")
    social_history=orm.Set(SocialHistory,reverse="condition")
    family_history=orm.Set(FamilyMedicalHistory,reverse="condition")
    radiologyAssesmentHistory=orm.Set(RadiologyAssesmentHistory,reverse="result")


class RadiologyAssesment(db.Entity):
    date=orm.Required(date)
    test_type=orm.Required("RadiologyAssesmentType")
    result=orm.Required(MedicalConditions)
    radiologist=orm.Required(GP)
    requesting_physician=orm.Required(GP)
    patients=orm.Required(Patient)

class DrugHistoryStatus(db.Entity):
    status=orm.Required(bool)


class RadiologyAssesmentType(db.Entity):
    name=orm.Required(str)
    assesments=orm.Set(RadiologyAssesment,reverse="test_type")

class Symptom(db.Entity):
    name=orm.Required(str)
    allergy=orm.Set(Allergy)

db.generate_mapping(create_tables=True)

