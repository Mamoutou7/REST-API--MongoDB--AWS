

from flask import Flask, jsonify, request
from flask_restful import Api, Resource

from pymongo import MongoClient
import bcrypt

app = Flask(__name__)
api = Api(app)


client = MongoClient('mongodb://db:27017')
db = client.SentencesDatabase
users = db["Users"]




class Register(Resource):
	"""docstring for Register"""
	def post(self):
		# Step 1 is to post data by the user
		postedData = request.get_json()

		# Get the data
		username = postedData["username"]
		password = postedData["password"]

		hashed_pw =bcrypt.hashpw(str(password).encode('utf-8'), bcrypt.gensalt())

		# Store username and pw into the database
		users.insert({
			"Username": username,
			"Password": hashed_pw,
			"Sentence": "",
			"Tokens": 6
			})

		retJSON = {
		"status": 200,
		"msg": "You successfully signed up for the API"
		}

		return jsonify(retJSON)


def verifyPw(username, password):
	hashed_pw = users.find({
		"Username":username
		})[0]["Password"]
	if bcrypt.hashpw(password.encode('utf-8'), hashed_pw) == hashed_pw:
		return True
	else:
		return False

def countTokens(username):
	tokens = users.find({
		"Username":username
		})[0]["Tokens"]
	return tokens


class Store(Resource):
	def post(self):
		# Step 1 is to post data b
		postedData = request.get_json()

		# Step 2 get the data
		username = postedData["username"]
		password = postedData["password"]
		sentence = postedData["sentence"]

		# Step 3 verify the username pw match
		correct_pw = verifyPw(username, password)
		if not correct_pw:
			retJSON = {
				"status": 302
			}
			return jsonify(retJSON)

		# Step 4 Verify user has enough tokens
		num_tokens = countTokens(username)
		if num_tokens <= 0:
			retJSON = {
				"status": 301
			}
			return jsonify(retJSON)

		# Step 5 store the sentence and return 2000K
		users.update({
			"Username":username
			}, {
			"$set":{
			"Sentence":sentence,
			"Tokens": num_tokens-1
			}
			})

		retJSON = {
			"status":200,
			"msg": "You saved successfully"
		}

		return jsonify(retJSON)


class Get(Resource):
	def post(self):
		# Step 1 is to post data 
		postedData = request.get_json()

		# Step 2 get the data
		username = postedData["username"]
		password = postedData["password"]
		
		# Step 3 verify the username pw match
		correct_pw = verifyPw(username, password)
		if not correct_pw:
			retJSON = {
				"status": 302
			}
			return jsonify(retJSON)

		# Step 4 Verify user has enough tokens
		num_tokens = countTokens(username)
		if num_tokens <= 0:
			retJSON = {
				"status": 301
			}
			return jsonify(retJSON)



		# MAKE THE USER PAY!
		users.update({
			"Username":username
			}, {
			"$set":{
			"Tokens": num_tokens-1
			}
			})

		retJSON = {
			"status":200,
			"msg": "You saved successfully"
		}

		return jsonify(retJSON)







		sentence = users.find({
			"Username": username
			})[0]["Sentence"]

		retJSON = {
			"status":200,
			"sentence": sentence
		}

		return jsonify(retJSON)




api.add_resource(Register, '/register')
api.add_resource(Store, '/store')
api.add_resource(Get, '/get')



if __name__ == '__main__':
		app.run(host='0.0.0.0')		
