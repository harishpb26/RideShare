from mongoengine import *
import datetime

class Ride(Document):
	rideId = IntField(min_value = 1, unique = True, required = True)
	username = StringField(required = True)
	users = ListField(StringField())
	timestamp = StringField()
	source = IntField(min_value = 1, max_value = 198, required = True)
	destination = IntField(min_value = 1, max_value = 198, required = True)

if __name__=="__main__":
	print("sUCCESS!")
