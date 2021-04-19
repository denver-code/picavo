import pymongo
from bson.objectid import ObjectId

#picavo_root 2oeTSzyEvU9dQ7FL

client = pymongo.MongoClient("mongodb+srv://picavo_root:2oeTSzyEvU9dQ7FL@cluster0.lrj3x.mongodb.net/picavo?retryWrites=true&w=majority")
db = client["picavo"]
users = db["users"]

def insert_db(db, data):
    return globals()[db].insert_one(data).inserted_id

def find(db, idc=None, uname=None, mail=None):
    if uname:
        return globals()[db].find_one({'username': uname})
    elif idc:
        return globals()[db].find_one({'_id': ObjectId(idc)})
    elif mail:
        return globals()[db].find_one({'email': mail})

def is_used(db, idc=None, uname=None, mail=None):
    if uname:
        return bool(globals()[db].find_one({'{}'.format(f'{db[:-1]}_name' if db != 'users' else 'username'): uname}))
    elif idc:
        return bool(globals()[db].find_one({'_id': ObjectId(idc)}))
    elif mail:
        return bool(globals()[db].find_one({'email': mail}))