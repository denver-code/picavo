import pymongo
from bson.objectid import ObjectId
from config import DATABASE, DATABASE_LOCAL
import requests

#? Для локалки mongodb://localhost:27017
r = requests.get('http://ip.42.pl/raw')
ip = r.text

if ip != "68.183.210.191":
    client = pymongo.MongoClient(DATABASE_LOCAL)
else:
    client = pymongo.MongoClient(DATABASE)

db = client["picavo"]
users = db["users"]
users.ensure_index([('UserID', 1), ('Email', 2)])

def insert_db(db, data):
    return globals()[db].insert_one(data).inserted_id


def find(db, idc=None, uname=None, mail=None):
    if uname:
        return globals()[db].find_one({"Username": uname})
    elif idc:
        return globals()[db].find_one({"UserID": idc})
    elif mail:
        return globals()[db].find_one({"Email": mail})


def update_db(db, scdata, ndata):
    return globals()[db].update_one(scdata, {"$set": ndata}, upsert=True)

def delete_db(db, obj):
    globals()[db].delete_one(obj)

def is_used(db, idc=None, uname=None, mail=None):
    if uname:
        return bool(globals()[db].find_one({"Username": uname}))
    elif idc:
        return bool(globals()[db].find_one({"UserID": idc}))
    elif mail:
        return bool(globals()[db].find_one({"Email": mail}))
