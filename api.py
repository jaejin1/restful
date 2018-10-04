from flask import Flask
from flask import jsonify
from flask import request
from flask_pymongo import PyMongo
import hashlib

app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'userdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/userdb'

mongo = PyMongo(app)

@app.route('/user/<hash>', methods=['GET'])
def get_one_star(hash):
  user = mongo.db.users
  a = user.find_one({'hash' : hash})
  if a:
    output = {'hash' : a['hash'],'name' : a['name'], 'number' : a['number']}
  else:
    output = "No such name and number"
  return jsonify({'result' : output})


@app.route('/user', methods=['POST'])
def add_user():
  user = mongo.db.users
  name = request.json['name']
  number = request.json['number']
  hash = hashlib.sha256(bytes("" + name + str(number), encoding='utf-8')).hexdigest()

  user_hash = user.insert({'name': name, 'number': number, 'hash': hash})
  new_user = user.find_one({'_id': user_hash })
  output = {'name': new_user['name'], 'number': new_user['number'], 'hash' : new_user['hash']}
  return jsonify({'result' : output})


if __name__ == '__main__':
    app.run(debug=True)