

from datetime import datetime

import jwt
from pony.orm import db_session, commit, select
from pony.orm.core import Entity, Set, Collection

from config import SECRET_KEY, REQUIRE_PERMISSION
from index import templates
from login import hash_pass
from models import *


def get_relations(entity_class):
    attrs=entity_class._adict_
    ret={}
    for attr in attrs:
       if attrs[attr].is_relation and attrs[attr].is_required:
           ret[attr]=attrs[attr].py_type
    return ret

def fetch_item(entity_class,item_id):
    """

        fetch one entity from database using the provided id
        :param entity_class:the table to fetch from

    """
    with db_session:
        try:
            entity = entity_class[item_id].to_dict(related_objects=True)
            if entity_class == History:
                entity["data"]=decode(entity.data)

            return to_json(entity)
        except Exception as e:
            print(e.args)
            return {"message":""}



def fetch_all_items(entity_class):

    """
    returns all elements in a table
    :param entity_class:
    :return:json object
    """

    with db_session:
        records = entity_class.select()
        return jsonify_query(records, True)


def _create_raw_item(entity_class,data):

    """

    :param entity_class: the class to fetch from
    :param data: a json object sent by the client containin all necessary data
    :return: a json object with the related entities  in as nested json objects
    """
    with db_session:

        entity={}

        relations=get_relations(entity_class)
        class_attrs=entity_class._adict_

        new_data={}

        for attr in data:
            if attr in class_attrs:
                entity[attr]=data[attr]
            else:
                new_data[attr]=data[attr]
        if new_data:
            for c in relations:
                if c not in data:
                    entity[c]=_create_raw_item(relations[c],new_data)
        return entity




def create_item(entity,data):
    """
    create new entity and save it into the database
    :param entity: entity clas
    :param data:a json object sent by the client containin all necessary data
    :return:Entity instance of type entity
    """
    #if entity in REQUIRE_PERMISSION:
     #   return {"message":"admin rights required"}

    with db_session:
        return_entity={}
        raw_item=_create_raw_item(entity,data)
        for raw_key,raw_value in raw_item.items():
            if isinstance(raw_value,dict):
                entity_type=entity._adict_[raw_key].py_type
                if entity_type.exists(**raw_value) and not raw_value=={}:
                    print(raw_value)
                    entity_instance=entity_type._find_one_(raw_value)
                else:
                    entity_instance=entity_type(**raw_value)
                    commit()
                return_entity[raw_key] = entity_instance.get_pk()
            else:
                if raw_key.lower()=="password":
                    raw_value=hash_pass(raw_value)
                return_entity[raw_key]=raw_value
        entity(**return_entity)
        return return_entity



def delete_item(entity_class,item_id):

    if entity_class in REQUIRE_PERMISSION:
        return {"message":"admin rights required"}

    with db_session:
        try:

            entity=entity_class[item_id]
            entity.delete()
            return {"message":"entity deleted"}

        except Exception as e:
            return {"message":"invalid item id"}

def update_item(entity_class,item_id,new_attributes):



    with db_session:
        try:

            entity=entity_class[item_id]

            data=encode(entity.to_dict())
            date=datetime.utcnow()
            class_name=entity.__class__.__name__
            history=History(entity_class=class_name,entity_id=entity.get_pk(),data=data,date=date)
            commit()
            for attr,value in new_attributes.items():

                if attr.lower()=="password":
                    value=hash_pass(value)
                setattr(entity,attr,value)
            return {"message":"item updated"}
        except:
            return {"message":"bad data or id"}




def encode(data):
    """converts json object to java web token"""
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


def decode(data):
    """converts web token to a json object"""
    return jwt.decode(data, SECRET_KEY, algorithms="HS256")


def to_json(entity_dict):
    data={}
    for key,val in entity_dict.items():
        if isinstance(val,Entity):
            if isinstance(val,GP):
                data[key]=to_json(val.to_dict(related_objects=True,exclude="password"))
            else:
                data[key]=to_json(val.to_dict(related_objects=True))
        else:
            data[key]="{}".format(val)

    return data

def jsonify_query(queryresult,protect_password=False):
    """recieves a pony.or(m.core.QueryResult and converts it
        json object
        :rtype: dict object
    """
    data={}
    for item in queryresult:
        index=item.get_pk()
        if isinstance(item,GP) and protect_password:
            item=item.to_dict(related_objects=True,exclude="password")
        else:
            item=item.to_dict(related_objects=True)
        data[index]=to_json(item)


    return data

def json_to_entity(ids_list,entity):
    """generates entities from a set of ids"""
    return [entity[id] for id in ids_list]

def token_sent(request):
    """returns a json if one was sent over a request"""
    if request.query:
        if  "token" in request.query.keys():
            data=request.query["token"]
            json=decode(data)
            return json
        return request.query

    return None

@db_session
def search_value_table(value,criteria):

    if criteria:
        cls=Patient._adict_[criteria]
        patients=[]
        if cls.is_basic:
            patients.extend(list(Patient.select(lambda p:getattr(p,criteria)==value)))
        else:
            print(criteria)
            s=getattr(Patient,criteria).py_type.select()
            for i in s:
                x=to_json(i.to_dict(related_objects=True))
                entity_values=[e.lower() for e in x.values() if not isinstance(e,dict)]

                if value in entity_values:

                    patients.extend(i.patients)
        return patients
    else:
        patients=[]
        for criteria in Patient._adict_:
            patients.extend(search_value_table(value,criteria))

    print(patients)




def fetch_template(entity,eid=None):
    if eid:
        key="i"+entity
    else:
        key=entity
    return templates[key]

if __name__=="__main__":
    search_value_table("1",None)