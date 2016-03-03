from flask import Flask,request,url_for
from  pymongo import MongoClient
import json

app = Flask(__name__)
client=MongoClient('localhost','27017')
@app.route('/api/getusers'):
	db=client.example
	users=db.users.find()
	result=[]
	for user in users:
		result.append(user)
	return json.dumps(result)


if __name__ == '__main__':
	app.run()
