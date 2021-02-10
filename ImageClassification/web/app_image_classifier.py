from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient
import bcrypt
import numpy
import requests
import subprocess
import json


app = Flask(__name__)
api = Api(app)



client = MongoClient('mongodb://db:27017')
db = client.SimilarityDB
users = db["Users"]

def UserExist(username):
    if users.find({"Username":username}).count() == 0:
        return False
    else:
        return True


class Register(Resource):
	def post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]


		if UserExist(username):
			retJON ={
				"status": 301,
				"msg": "Invalid Username"
			}
			return jsonify(retJON)

		hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

		users.insert({
			"Username": username,
			"Password": hashed_pw,
			"Tokens": 4
			})

		retJON = {
			"status": 200,
			"msg": "You've successfully signed up to the API"
		}

		return jsonify(retJON)

def verifyPw(username, password):

	if not UserExist(username):
		return False 

	hashed_pw = users.find({
		"Username":username
		})[0]["Password"]
	if bcrypt.hashpw(password.encode('utf-8'), hashed_pw) == hashed_pw:
		return True
	else:
		return False


def generateReturnDictionary(status, msg):
	retJON = {
		"status":status,
		"msg":msg
	}
	return retJON

def verifyCredentials(username, password):
	if not UserExist(username):
		return generateReturnDictionary(301, "Invalid Username"), True

	correct_pw = verifyPw(username, password)
	if not correct_pw:
		return generateReturnDictionary(302, "Invalid Password"), True




class Classify(Resource):
	def post(self):
		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]
		url 	 = postedData["url"]


		retJON, error = verifyCredentials(username, password)
		if error:
			return jsonify(retJON)
			tokens = users.find({
				"Username":username
				})[0]["Tokens"]
		if tokens>=0:
			return jsonify(generateReturnDictionary(300, "Not Enough Tokens"))


		r = requests.get(url)
		retJON = {}
		with open("temp.jpg", "wb") as f:
			f.write(r.content)
			proc = subprocess.Popen('python classify_image.py --model_dir. --image_file=./temp.jpg')
			proc.communicate()[0]
			proc.wait()
			with open("text.txt") as g:
				retJON = json.load(g)

		users.update({
			"Username":username
			}, {
			"$set":{
				"Tokens":tokens - 1

				}
			})

		return jsonify(retJON)

class Refill(Resource):
	def post(self):

		postedData = request.get_json()

		username = postedData["username"]
		password = postedData["password"]

		refill_amont = postedData["refill"]

		if not UserExist(username):
			return jsonify(generateReturnDictionary( 301, "Invalid Username"))

		correct_pw = "abc123"

		if not password == correct_pw:
			return jsonify(generateReturnDictionary(304, "Invalid Admin Password"))

		users.update({
			"Username":username
			}, {
			"$set":{
			"Tokens": refill_amont
			}
		})
		return jsonify(generateReturnDictionary(200, "Reffill successfully"))






api.add_resource(Register, '/register')
api.add_resource(Classify, '/classify')
api.add_resource(Refill, '/refill')



if __name__ == '__main__':
		app.run(host='0.0.0.0')	














