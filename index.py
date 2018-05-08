import json

from pony.orm import db_session

from models import *

templates={
    "iadmin_GP":"gp.html",
    "admin_GP":"aUTable.html",
    "idrug_history":"drugProfile.html",
    "patients":"plist.html",
    "ipatients":"patientProfile.html",
    "add_medreport":"CreateCReport.html",
    "imedhistory":"cRecord.html",
    "medhistory":"medicalHList.html",
    "patient_drug_history":"drugHist.html",
    "patient_allergy":"allergylist.html",
    "radiology":"radiologylist.html",
    "patient_medhistory":"medhistlist.html",
    "patient_socialhistory":"socialHist.html",
    "socialhistory":"createSocialHist.html",
    "add_patients":"pcreate.html",
    "add_users":"addGP.html",
    "admin_users":"aUTable.html",
    "admin_patients":"table.html",
    "admin_drug":"aDTable.html",
    "admin_medConditions":"aMCtable.html",
    "admin_radiology":"aRTable.html",
    "edit_medreport":"editCReport.html",
    "patient_familyhistory":"famHistList.html",
    "patient_radiology":"radiologylist.html",

}

ENTITY_DICT={
    "patient":Patient,
    "patients":Patient,
    "addresses":Address,
    "users":GP,
    "medhistory":Medicalhistory,
    "familyhistory":FamilyMedicalHistory,
    "allergy":Allergy,
    "radiology":RadiologyAssesment,
    "radiolgytype":RadiologyAssesmentType,
    "drug":Drug,
    "drughistorystatus":DrugHistoryStatus,
    "drug_history":DrugHistory,
    "institution":Institution,
    "disrict":District,
    "address":Address,
    "history":History,
    "GP":GP,
    "symptom":Symptom,
    "socialhistory":SocialHistory,
    "medConditions":MedicalConditions,

}

