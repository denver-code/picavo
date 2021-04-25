import pymongo
from bson.objectid import ObjectId
from config import DATABASE

#? Для локалки mongodb://localhost:27017
client = pymongo.MongoClient(DATABASE)
db = client["picavo"]
users = db["users"]


def insert_db(db, data):
    return globals()[db].insert_one(data).inserted_id


def find(db, idc=None, uname=None, mail=None):
    if uname:
        return globals()[db].find_one({"username": uname})
    elif idc:
        return globals()[db].find_one({"_id": ObjectId(idc)})
    elif mail:
        return globals()[db].find_one({"email": mail})


def update_db(db, scdata, ndata):
    return globals()[db].update_one(scdata, {"$set": ndata}, upsert=True)


def is_used(db, idc=None, uname=None, mail=None):
    if uname:
        return bool(
            globals()[db].find_one(
                {"{}".format(f"{db[:-1]}_name" if db != "users" else "username"): uname}
            )
        )
    elif idc:
        return bool(globals()[db].find_one({"_id": ObjectId(idc)}))
    elif mail:
        return bool(globals()[db].find_one({"email": mail}))
