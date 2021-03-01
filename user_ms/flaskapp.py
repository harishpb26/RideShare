import copy
from flask import Flask, render_template, jsonify, request, abort
from bson.json_util import loads, dumps
from bson import Binary, Code
import mongoengine
import dbapi
import datetime
import requests
import re

dbapi.myconnect()
app = Flask(__name__)

ride_ms = "ride_ms"
user_ms = "user_ms"

@app.route('/api/v1/users', methods = ["GET"])
def list_users():
    r1 = requests.post("http://%s/api/v1/db/read"%user_ms, json = {"collection":"User", "jsonobj" : {}, "fields":[]})
    if len(r1.json())==0:
        return jsonify([]), 204
    else:
        return jsonify(list(map(lambda x:x["username"], r1.json()))), 200

@app.route('/api/v1/users', methods = ["PUT"])
# Status codes 201, 400, 405, 500
def add_user():
    # Getting requried objects from request
    user = dict()
    user["username"] = request.get_json()["username"]
    user["password"] = request.get_json()["password"]

    # check if the user already exists
    r1 = requests.post("http://%s/api/v1/db/read"%user_ms, json = {"collection":"User", "jsonobj" : {"username" : user["username"]}, "fields":[]})
    if len(r1.json())!=0: #someone check this later
        return "User already exists!", 400

    # check if the password is in the required format
    if not re.compile("^[a-fA-F0-9]{40}$").match(user["password"]):
        return "Password format incorrect", 400

    # write the user object to the database
    r = requests.post("http://%s/api/v1/db/write"%user_ms, json = {"collection":"User", "jsonobj" : user, "action":"insert"})

    if r.status_code == 200:
        return jsonify({}), 201
    else:
        return "Please check input", 400

@app.route('/api/v1/users/<username>', methods = ["DELETE"])
# Status codes 200,400,405
def remove_user(username):
    # check if the user exists in the database
    r1 = requests.post("http://%s/api/v1/db/read"%user_ms, json = {"collection":"User", "jsonobj" : {"username" : username}, "fields":[]})
    if len(r1.json())==0: # someone check this later
        return "Username does not exist", 400

    # delete the user from the database
    r = requests.post("http://%s/api/v1/db/write"%user_ms, json = {"collection":"User", "jsonobj" : {"username":username} , "action":"delete"})
    # if the user was deleted, delete his other stuff
    if r.status_code == 200:
        requests.post("http://%s/api/v1/db/write"%ride_ms, json = {"collection":"Ride", "jsonobj" : {"username":username} , "action":"delete"})
        r =requests.post("http://%s/api/v1/db/read"%ride_ms, json = {"collection":"Ride", "jsonobj" : {} , "fields":[]})
        cpy = copy.deepcopy(r.json())
        for obj in cpy:
            if username in obj["users"]:
                obj["users"].remove(username)
        requests.post("http://%s/api/v1/db/write"%ride_ms, json = {"collection":"Ride", "jsonobj" :cpy , "action":"update"})
        return jsonify({}), 200

    elif r.status_code==204:
        return "User not present",400
    else:
        return "Delete operation failed", 400

@app.route('/api/v1/db/write', methods=["POST"])
def write_db():
    # Getting requried objects from request

    action = request.get_json()["action"]
    jsonobj = request.get_json()["jsonobj"]
    collection = request.get_json()["collection"]

    if action == "delete":
        try:
            dbapi.delete(collection, jsonobj)
        except mongoengine.errors.DoesNotExist:
            return jsonify({}), 200
        else:
            return jsonify({}), 200

    elif action == "insert":
        try:
            dbapi.insert(collection, jsonobj)
        except (mongoengine.errors.ValidationError, mongoengine.errors.NotUniqueError):
            return "Insert Error", 400
        else:
            return jsonify({}), 200
    elif action == "update":
        dbapi.update(collection, jsonobj)
        return jsonify({}), 200

@app.route('/api/v1/db/read',methods=["POST"])
def read_db():
    # Getting requried objects from request
    collection = request.get_json()["collection"]
    jsonobj = request.get_json()["jsonobj"]
    fields = request.get_json()["fields"]

    return dbapi.query(collection, jsonobj, fields), 200, {"Content-type":"application/json"}

@app.route('/api/v1/db/clear', methods = ["POST"])
def cleardb():
    requests.post("http://%s/api/v1/db/write"%user_ms, json={"collection":"User", "jsonobj" : {} , "action":"delete"})
    return jsonify({}), 200

if __name__ == '__main__':
    app.debug=True
    # app.run()
    app.run(host = "0.0.0.0", port=80) # localhost or 127.0.0.1 or change the IP and PORT number also...
