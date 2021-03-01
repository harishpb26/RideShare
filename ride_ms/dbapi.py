import json
import re
from mongoengine import *
from Schema.Ride import Ride
import mongoengine.errors

pattern = re.compile(r'"_id":[^,]*,')

def myconnect():
	connect('mongoengine_test', host='mongo_ride:27017')
def mydisconnect1():
	connection.disconnect(alias = "conn")

def insert(coll, obj):
	# Inserts the given document
	if coll=="Ride":
			# obj["rideId"] = Ride.objects.count()+1
		if Ride.objects().count()>0:
			obj["rideId"] = Ride.objects().order_by("-rideId").limit(-1).first().rideId+1
			# print("rideId", Ride.objects().order_by("rideId").limit(-1).first().rideId)
			# obj["rideId"] = max([i.rideId for i in Ride.objects()]) + 1
		else:
			obj["rideId"] =1
	exec("u = %s(**obj); u.save()" % coll)

def query(coll,queryobj={}, queryfields=[]):
	# returns a list of objects that match the given query JSON object
	# returns both Ride and User

	if len(queryfields)==0:
		retval = json.loads( eval("%s.objects(**queryobj)"%coll).to_json())
		for i in retval:
			i.pop("_id", None)
		return json.dumps(retval)
	retval = json.loads(eval("%s.objects(**queryobj).only(*queryfields)"%coll).to_json())
	for i in retval:
		i.pop("_id", None)
	return json.dumps(retval)

def delete(coll, queryobj):
	u = list(eval("%s.objects(**queryobj)"%coll))
	print(u)
	for entry in u:
		entry.delete()
	if len(u)==0:
		raise mongoengine.errors.DoesNotExist()

def update(coll, mylist):
	if coll == "Ride":
		print(mylist)
		for myobj in mylist:
			ride = Ride.objects(rideId = myobj["rideId"])[0]
			ride.users = myobj["users"]
			ride.save()

if __name__=="__main__":
	# usage  of the API
	# dont use disconnect for now
	myconnect()
	a = dict()
	a['username'] = '12332'
	a['source'] = 1
	a["destination"] = 2
	a['users'] = ["a", "b", "c"]
	# insert("Ride", a)
	# this gives us a list of Users that satisfy the query JSON
	# print(query("User", {"username":"y0"}))
	# delete("User", {"username":"y0y0"})
	# print(query("User", {}, ["username"])[0]["password"])
