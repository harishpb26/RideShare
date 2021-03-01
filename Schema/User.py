from mongoengine import *
import re

regexp = re.compile('[a-fA-F0-9]{40}')

class User(Document):
	username = StringField(unique = True, required = True)
	password = StringField(required = True, regex = regexp)

if __name__=="__main__":
	connect('mongoengine_test', host='localhost:27017')
	user = User(username = "y0")
	user.save()
	print("sUCCESS!")
